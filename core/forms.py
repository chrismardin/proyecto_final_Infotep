from django import forms
from .models import MovimientoStock, MovimientoFinanciero, Producto


class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['producto', 'tipo', 'cantidad', 'motivo']
        widgets = {
            'producto': forms.Select(attrs={'class': 'select-producto'}),
            'tipo': forms.Select(attrs={'class': 'select-tipo'}),
            'cantidad': forms.NumberInput(attrs={'min': 1}),
            'motivo': forms.TextInput(attrs={'placeholder': 'Ej. Compra a proveedor, Venta, Ajuste...'}),
        }


class MovimientoFinancieroForm(forms.ModelForm):
    class Meta:
        model = MovimientoFinanciero
        fields = ['tipo', 'fecha', 'categoria', 'cliente_proveedor', 'monto', 'medio_pago', 'factura']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Ej. Venta Laptop, Pago Luz...'}),
            'cliente_proveedor': forms.TextInput(attrs={'placeholder': 'Nombre del cliente o proveedor'}),
            'factura': forms.TextInput(attrs={'placeholder': 'Opcional'}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'categoria', 'costo_compra', 'precio_venta', 'stock', 'stock_minimo']
        widgets = {
            'sku': forms.TextInput(attrs={'placeholder': 'Ej. L006'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del producto'}),
            'costo_compra': forms.NumberInput(attrs={'step': '0.01'}),
            'precio_venta': forms.NumberInput(attrs={'step': '0.01'}),
        }