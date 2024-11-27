from django.contrib import admin
from .models import *

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad', 'estado_entrega', 'fecha_pedido')
    list_filter = ('estado_entrega',)
    search_fields = ('usuario__username', 'producto__nombre')

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Producto)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Pagina)
admin.site.register(PaginaNosotros)

