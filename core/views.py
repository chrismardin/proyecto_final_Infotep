from django.shortcuts import render, redirect
from django.db import models
from .models import Producto, MovimientoStock, MovimientoFinanciero, ProductoVentaHistorial
from .forms import MovimientoStockForm


from django.utils.timezone import now

def dashboard(request):
    movimientos = MovimientoFinanciero.objects.all()[:5]

    ingresos = MovimientoFinanciero.objects.filter(tipo='Ingreso')
    gastos = MovimientoFinanciero.objects.filter(tipo='Gasto')

    total_ingresos = sum(float(m.monto) for m in ingresos if m.monto is not None)
    total_gastos = sum(float(m.monto) for m in gastos if m.monto is not None)
    ganancia_neta = total_ingresos - total_gastos

    hoy = now().date()
    ventas_mes = MovimientoFinanciero.objects.filter(
        tipo="Ingreso",
        categoria="Ventas",
        fecha__month=hoy.month,
        fecha__year=hoy.year
    )
    total_ventas_mes = sum(float(v.monto) for v in ventas_mes if v.monto is not None)

    return render(request, 'core/dashboard.html', {
        'movimientos': movimientos,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'ganancia_neta': ganancia_neta,
        'total_ventas_mes': total_ventas_mes,
    })

def inventario(request):
    if request.method == 'POST':
        form = MovimientoStockForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            producto = movimiento.producto

            if movimiento.tipo == 'Entrada':
                producto.stock += movimiento.cantidad
            else:  # Salida
                if movimiento.cantidad > producto.stock:
                    form.add_error('cantidad', 'No hay suficiente stock para esta salida.')
                    return render(request, 'core/inventario.html', {
                        'productos': Producto.objects.all(),
                        'form': form,
                        'movimientos': MovimientoStock.objects.all()[:20],
                        'historial': MovimientoStock.objects.all(),
                        **_contexto_kpis(),
                    })
                producto.stock -= movimiento.cantidad

            producto.save()
            movimiento.save()
            return redirect('inventario')
    else:
        form = MovimientoStockForm()

    lista_productos = Producto.objects.all()
    movimientos = MovimientoStock.objects.all()[:20]

    return render(request, 'core/inventario.html', {
        'productos': lista_productos,
        'form': form,
        'movimientos': movimientos,
        'historial': MovimientoStock.objects.all(),
        **_contexto_kpis(),
    })


def _contexto_kpis():
    lista_productos = Producto.objects.all()
    return {
        'total_productos': lista_productos.count(),
        'bajo_stock': lista_productos.filter(stock__lt=models.F('stock_minimo')).count(),
        'valor_total': sum(p.costo_compra * p.stock for p in lista_productos),
    }


def proyecciones(request):
    return render(request, 'core/proyecciones.html')


def clientes(request):
    return render(request, 'core/clientes.html')


def empleados(request):
    return render(request, 'core/empleados.html')


def reportes(request):
    return render(request, 'core/reportes.html')


def configuracion(request):
    return render(request, 'core/configuracion.html')






from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def procesar_venta(request):
    if request.method == "POST":
        data = json.loads(request.body)

        subtotal = data.get("subtotal", 0)
        itbis = data.get("itbis", 0)
        total = data.get("total", 0)
        productos = data.get("productos", [])

        # Guardar movimiento financiero
        MovimientoFinanciero.objects.create(
            tipo="Ingreso",
            fecha=data.get("fecha", now().date()),  # usa fecha actual si no llega
            categoria="Ventas",
            cliente_proveedor=data.get("cliente", "Cliente Genérico"),
            monto=total,
            medio_pago=data.get("medio_pago", "Efectivo"),
            factura=data.get("factura", "")
        )

        # Actualizar stock y registrar movimientos
        for p in productos:
            try:
                producto = Producto.objects.get(sku=p["sku"])
                producto.stock -= int(p["cantidad"])
                producto.save()

                MovimientoStock.objects.create(
                    producto=producto,
                    tipo="Salida",
                    cantidad=int(p["cantidad"]),
                    motivo="Venta"
                )
            except Producto.DoesNotExist:
                continue

        return JsonResponse({"mensaje": "¡Venta guardada en la base de datos!"})

def productos(request):
    lista_productos = Producto.objects.all()
    return render(request, 'core/productos.html', {'productos': lista_productos})


def ventas(request):
    # Cargamos el historial de productos guardado en la base de datos
    # para que la pestaña "Historial" lo muestre apenas se abre la pagina.
    historial = list(
        ProductoVentaHistorial.objects.all().values('sku', 'nombre', 'precio')
    )
    # Los DecimalField no son JSON-serializables por defecto, los pasamos a float.
    for item in historial:
        item['precio'] = float(item['precio'])

    return render(request, 'core/ventas.html', {
        'historial_json': historial,
    })


def finanzas(request):
    return render(request, 'core/finanzas.html')


@csrf_exempt
def guardar_historial_producto(request):
    """Crea o actualiza (por SKU) un producto en el historial de ventas."""
    if request.method != "POST":
        return JsonResponse({"error": "Metodo no permitido"}, status=405)

    data = json.loads(request.body)
    sku = (data.get("sku") or "").strip()
    nombre = (data.get("producto") or data.get("nombre") or "").strip()
    precio = data.get("precio", 0)

    if not sku or not nombre:
        return JsonResponse({"error": "SKU y nombre son obligatorios"}, status=400)

    ProductoVentaHistorial.objects.update_or_create(
        sku=sku,
        defaults={"nombre": nombre, "precio": precio},
    )
    return JsonResponse({"mensaje": "Producto guardado en el historial"})


@csrf_exempt
def borrar_historial_producto(request):
    """Elimina un producto del historial de ventas por SKU."""
    if request.method != "POST":
        return JsonResponse({"error": "Metodo no permitido"}, status=405)

    data = json.loads(request.body)
    sku = (data.get("sku") or "").strip()
    ProductoVentaHistorial.objects.filter(sku=sku).delete()
    return JsonResponse({"mensaje": "Producto eliminado del historial"})


@csrf_exempt
def resetear_ventas_mes(request):
    """Elimina los ingresos de categoria 'Ventas' registrados este mes,
    para que el KPI 'Ventas del Mes' del dashboard vuelva a cero."""
    if request.method != "POST":
        return JsonResponse({"error": "Metodo no permitido"}, status=405)

    hoy = now().date()
    eliminados, _ = MovimientoFinanciero.objects.filter(
        tipo="Ingreso",
        categoria="Ventas",
        fecha__month=hoy.month,
        fecha__year=hoy.year,
    ).delete()

    return JsonResponse({"mensaje": "Ventas del mes reiniciadas", "eliminados": eliminados})
