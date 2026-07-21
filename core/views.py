from django.shortcuts import render, redirect
from django.db import models
from .models import Producto, MovimientoStock, MovimientoFinanciero
from .forms import MovimientoStockForm


def dashboard(request):
    movimientos = MovimientoFinanciero.objects.all()[:5]

    ingresos = MovimientoFinanciero.objects.filter(tipo='Ingreso')
    gastos = MovimientoFinanciero.objects.filter(tipo='Gasto')

    total_ingresos = sum(m.monto for m in ingresos)
    total_gastos = sum(m.monto for m in gastos)
    ganancia_neta = total_ingresos - total_gastos

    return render(request, 'core/dashboard.html', {
        'movimientos': movimientos,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'ganancia_neta': ganancia_neta,
    })


def productos(request):
    lista_productos = Producto.objects.all()
    return render(request, 'core/productos.html', {'productos': lista_productos})


def ventas(request):
    return render(request, 'core/ventas.html')


def finanzas(request):
    return render(request, 'core/finanzas.html')


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