from django.shortcuts import render
from django.views.generic import TemplateView
from . import functions
from django.contrib import messages
from cuenta.models import Pagina


class index(TemplateView):
    template_name = "inicio/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagina = Pagina.objects.first()
        context['pagina'] = pagina
        return context
    
    def post(self, request, *args, **kwargs):
        producto = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        ciudad = request.POST.get("ciudad")
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        empresa = request.POST.get("empresa")
        mensaje = request.POST.get("mensaje")
        functions.aviso_cotizacion(producto,cantidad,ciudad,nombre,correo,telefono,empresa,mensaje)
        functions.enviar_correo(producto,cantidad,ciudad,nombre,correo,telefono,empresa,mensaje)
        return render(request, self.template_name)

def nosotros(request):
    return render(request, "inicio/nosotros.html")

class productos(TemplateView):
    template_name = "inicio/productos.html"
    
    def post(self, request, *args, **kwargs):
        producto = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        ciudad = request.POST.get("ciudad")
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        empresa = request.POST.get("empresa")
        mensaje = request.POST.get("mensaje")
        functions.aviso_cotizacion(producto,cantidad,ciudad,nombre,correo,telefono,empresa,mensaje)
        functions.enviar_correo(producto,cantidad,ciudad,nombre,correo,telefono,empresa,mensaje)
        return render(request, self.template_name)

class contacto(TemplateView):
    template_name = "inicio/contacto.html"
    
    def post(self, request, *args, **kwargs):
        producto = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        ciudad = request.POST.get("ciudad")
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        empresa = request.POST.get("empresa")
        mensaje = request.POST.get("mensaje")
        functions.aviso_cotizacion(producto,cantidad,ciudad,nombre,correo,telefono,empresa,mensaje)
        functions.enviar_correo(producto,cantidad,ciudad,nombre,correo,telefono,empresa,mensaje)
        return render(request, self.template_name)
