from django import forms
from .models import MovimientoStock


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