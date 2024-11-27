from django import forms
from .models import *

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar productos disponibles (puedes agregar más filtros si es necesario)
        self.fields['producto'].queryset = Producto.objects.filter(stock__gt=0)
        


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock']
        
        
class PaginaForm(forms.ModelForm):
    class Meta:
        model = Pagina
        fields = ['titulo', 'titulo_dos','color_letra_titulo','color_letra_titulo_dos','color_boton','color_letra_boton','imagen_inicio']
        

class PaginaFormNosotros(forms.ModelForm):
    class Meta:
        model = PaginaNosotros
        fields = ['titulo', 'titulo_dos','color_letra_titulo','color_letra_titulo_dos','txt_uno','txt_dos','color_txt_uno','color_txt_dos']
        
        
class PaginaFormProductos(forms.ModelForm):
    class Meta:
        model = PaginaProductos
        fields = ['color_letra_titulo', 'color_letra_titulo_dos','color_btn','color_letra_btn']
        

class PaginaFormContacto(forms.ModelForm):
    class Meta:
        model = PaginaContacto
        fields = ['color_letra_titulo', 'color_letra_titulo_dos','color_btn','color_letra_btn']