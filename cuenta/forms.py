from django import forms
from .models import Pedido, Producto

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar productos disponibles (puedes agregar más filtros si es necesario)
        self.fields['producto'].queryset = Producto.objects.filter(stock__gt=0)