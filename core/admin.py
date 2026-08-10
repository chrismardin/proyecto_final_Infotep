from django.contrib import admin
<<<<<<< Updated upstream
from .models import Producto, MovimientoStock, MovimientoFinanciero, ProductoVentaHistorial
=======
from .models import Producto, MovimientoStock, MovimientoFinanciero, Cliente, Venta, DetalleVenta
>>>>>>> Stashed changes


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'categoria', 'precio_venta', 'stock', 'estado_stock')
    list_filter = ('categoria',)
    search_fields = ('sku', 'nombre')


@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'producto', 'tipo', 'cantidad', 'motivo')
    list_filter = ('tipo',)


@admin.register(MovimientoFinanciero)
class MovimientoFinancieroAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'categoria', 'cliente_proveedor', 'monto', 'medio_pago')
    list_filter = ('tipo', 'medio_pago')
    search_fields = ('categoria', 'cliente_proveedor', 'factura')


<<<<<<< Updated upstream
@admin.register(ProductoVentaHistorial)
class ProductoVentaHistorialAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'precio', 'actualizado')
    search_fields = ('sku', 'nombre')
=======
 
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'telefono', 'tipo')
    search_fields = ('nombre', 'empresa')


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'cliente', 'total', 'metodo_pago')
    inlines = [DetalleVentaInline]   
>>>>>>> Stashed changes
