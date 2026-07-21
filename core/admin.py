from django.contrib import admin
from .models import Producto, MovimientoStock, MovimientoFinanciero


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