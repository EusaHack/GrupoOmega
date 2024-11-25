from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.contrib.auth import logout,get_user_model,login
from .models import CustomUser,Producto,Pedido
from . import functions_x
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PedidoForm,ProductoForm
from django.http import JsonResponse
import json 
from .models import Producto, Pedido
from django.db.models import Sum
from django.contrib import messages
from datetime import datetime

# Create your views here.

User = get_user_model()

@login_required()
def prueba_mensaje(request):
    return HttpResponse('Hola mundo')


@login_required()
def usuario_dashboard(request):
    if request.user.is_superuser:
        return redirect(reverse('usuario_dashboard_admin'))
    else:
        return redirect(reverse('user_dashboard_user'))
    

class usuario_dashboard_no_admin(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/user.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context

class usuario_pedidos(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/user-pedidos.html'
    
    def get(self, request, *args, **kwargs):
        pedidos = Pedido.objects.filter(usuario=request.user)
        form = PedidoForm()
        return render(request, self.template_name, {'form': form, 'pedidos': pedidos})
    
    def post(self, request, *args, **kwargs):
        form = PedidoForm(request.POST)
        if form.is_valid():
            
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.save()
            
            producto = pedido.producto
            producto.stock -= pedido.cantidad
            producto.save()
            
            form = PedidoForm()
            
            pedidos = Pedido.objects.filter(usuario=request.user)
            
            return render(request, self.template_name,{'form': form, 'pedidos': pedidos})
        
        return render(request, self.template_name, {'form': form, 'pedidos': pedidos})
class usuario_perfil(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/user-perfil.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['email'] = self.request.user.email
        context['number'] = self.request.user.number
        return context
    
    def post(self, request, *args, **kwargs):
        # Verificar si la solicitud es AJAX mediante el encabezado X-Requested-With
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            username = request.POST.get('username')  
            email = request.POST.get('email')
            number = request.POST.get('number')

            if username:
                request.user.username = username
                request.user.save()
            if email:
                request.user.email = email
                request.user.save()
            if number:
                request.user.number = number
                request.user.save()

            return JsonResponse({'success': True, 'message': 'Datos actualizados correctamente.'})
        else:
            return JsonResponse({'success': False, 'message': 'No es una solicitud AJAX válida.'})

        
class usuario_dashboard_admin(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/admin.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context

class DashBoardView(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/admin-d.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos = Producto.objects.all()

        ventas_por_producto = Pedido.objects.values('producto__nombre') \
                                             .annotate(total_ventas=Sum('cantidad')) \
                                             .order_by('producto__nombre')

        productos_nombres = [venta['producto__nombre'] for venta in ventas_por_producto]
        cantidades_por_producto = [venta['total_ventas'] for venta in ventas_por_producto]


        context['productos_nombres'] = productos_nombres
        context['cantidades_por_producto'] = cantidades_por_producto

        return context
    
class ModifView(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/admin-m.html'
    

class ProductosView(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/admin-p.html'
    
    def get(self, request, *args, **kwargs):
        form = ProductoForm()
        productos = Producto.objects.all()
        return self.render_to_response({'form': form, 'productos': productos})
    
    def post(self, request, *args, **kwargs):
        form = ProductoForm(request.POST or None)  
        if 'eliminar' in request.POST:  
            producto_id = request.POST.get('producto_id')
            producto = get_object_or_404(Producto, pk=producto_id)
            producto.delete()
            messages.success(request, 'Producto eliminado correctamente.')
            form = ProductoForm()
        
        else:  
            form = ProductoForm(request.POST)
            if form.is_valid():
                form.save() 
                messages.success(request, 'Producto agregado correctamente.')
                form = ProductoForm()  

        productos = Producto.objects.all()
        return render(request, self.template_name, {'form': form, 'productos': productos})

class PedidosView(LoginRequiredMixin, TemplateView):
    template_name = 'cuenta/admin-pe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedidos'] = Pedido.objects.all()  
        return context

    def post(self, request, *args, **kwargs):
        pedido_id = request.POST.get("pedido_id")
        razon_cancelacion = request.POST.get("razon_cancelacion")
        confirmacion_entrega = request.POST.get("confirmacion_entrega")
        nuevo_estado = request.POST.get("estado_entrega", "pendiente")
        fecha_hoy = datetime.now().date()
        if pedido_id:
            try:
                pedido = Pedido.objects.get(id=pedido_id)
                if razon_cancelacion:
                    pedido.estado_entrega = "cancelado"
                    pedido.razon_cancelacion = razon_cancelacion
                    producto = pedido.producto
                    producto.stock += pedido.cantidad
                    producto.save()
                    functions_x.envio_correo_estatus_pedido(pedido.usuario.email,pedido.estado_entrega,pedido.id,razon_cancelacion,fecha_hoy, pedido.producto.nombre)
                elif confirmacion_entrega:
                    pedido.estado_entrega = "entregado"
                    pedido.confirmacion_entrega = confirmacion_entrega
                    functions_x.envio_correo_estatus_pedido(pedido.usuario.email,pedido.estado_entrega,pedido.id,confirmacion_entrega,fecha_hoy,pedido.producto.nombre)
                else:
                    if nuevo_estado == "en progreso":
                        functions_x.envio_correo_estatus_pedido(pedido.usuario.email,nuevo_estado,pedido.id,razon_cancelacion,fecha_hoy,pedido.producto.nombre)
                    pedido.estado_entrega = nuevo_estado
                pedido.save()
            except Pedido.DoesNotExist:
                print(f"No se encontró el pedido con ID {pedido_id}")

        return redirect("pedidos_admin")

class ModificacionesUsuariosVista(LoginRequiredMixin, TemplateView):
    template_name = 'cuenta/admin-users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = CustomUser.objects.exclude(is_superuser=True)  # Pasa todos los usuarios al template
        return context
    
    def post(self, request, *args, **kwargs):
        if 'eliminar' in request.POST:
            user_id = request.POST.get('user_id')  # Obtener el ID del usuario desde el formulario
            usuario = get_object_or_404(CustomUser, pk=user_id)  # Obtener el usuario o devolver 404
            usuario.delete()  # Eliminar el usuario
            messages.success(request, "Usuario eliminado correctamente.")
            return redirect('usuarios_admin')  # Redirigir a la misma vista después de eliminar
        if 'modificar' in request.POST:
            user_id = request.POST.get('user_id')  # Obtener el ID del usuario
            usuario = get_object_or_404(CustomUser, pk=user_id)
            usuario.username = request.POST.get(f'username-{user_id}', usuario.username)
            usuario.email = request.POST.get(f'email-{user_id}', usuario.email)
            usuario.name_business = request.POST.get(f'name_business-{user_id}', usuario.name_business)
            usuario.number = request.POST.get(f'number-{user_id}', usuario.number)
            usuario.save()  # Guardar los cambios en la base de datos

            messages.success(request, "Usuario modificado correctamente.")
            return redirect('usuarios_admin')
        
        messages.error(request, "No se pudo procesar la solicitud.")
        return redirect('usuarios_admin')

def salir(request):
    logout(request)
    return redirect('/')


def authorization(request):
    return render(request, 'cuenta/codeAuth.html')

def authorizationUser(request):
    if request.method == 'POST':
        global bussines_auth,email_auth
        bussines_auth = request.POST.get('bussines_auth')
        email_auth = request.POST.get('email_auth')
        user_email = CustomUser.objects.filter(email=email_auth).first()
        user_bussines = CustomUser.objects.filter(name_business=bussines_auth).first()
        
        if bussines_auth == "" or email_auth == "" or bussines_auth.isspace() or email_auth.isspace():
            return render(request, 'cuenta/codeAuth.html')
        if user_email or user_bussines:
            return render(request, 'cuenta/userPasswordExist.html')
        else:
            global numero_random_auth
            numero_random_auth = functions_x.generador_numero()
            functions_x.envio_code_auth(numero_random_auth,bussines_auth,email_auth)
            return render(request, 'cuenta/registerAuth.html')
        
def codeUserValidation(request):
    if request.method == 'POST':
        code_auth = request.POST.get('code_auth')
        
        if numero_random_auth == int(code_auth):
            return render(request, 'cuenta/register.html')
        else:
            return render(request, 'cuenta/codeInvalid.html')
    raise Http404("Página no encontrada")

def create_new_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        hashed_password = make_password(password)
        user = CustomUser.objects.create(username = name, name_business = bussines_auth,
            email = email_auth, number = phone_number, password = hashed_password)
        user.save()
        return render(request, 'cuenta/succes.html')
    else:
        raise Http404("Página no encontrada")
    
def reset_password(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        global email_reset
        email_reset = request.POST['date_email']
        email_user = CustomUser.objects.filter(email=email_reset).first()
        
        if email_reset == "" or email_reset.isspace():
            return render(request, 'cuenta/login.html')
        
        if email_user:
            if action == 'numero':
                global numero_random_reset
                numero_random_reset = functions_x.generador_numero()
                functions_x.envio_correo(numero_random_reset,email_reset)
                return render(request, 'cuenta/reset.html')
        else:
            return render(request, 'cuenta/emailDoesNotExist.html')
    else:
        raise Http404("Página no encontrada")
    
def validar_numero(request):
    if request.method == 'POST':
        data_number = request.POST.get('validate_data')
        if numero_random_reset == int(data_number):
            return render(request, 'cuenta/resetUser.html')
        else:
            return render(request, 'cuenta/codeInvalid.html')
    else:
        raise Http404("Página no encontrada")
    
def change_password(request):
    if request.method == 'POST':
        pass_change = request.POST.get('passChange')
        user = get_object_or_404(CustomUser, email=email_reset)
        user.password = make_password(pass_change)
        user.save()
        return render(request, 'cuenta/changePass.html')
    else:
        raise Http404("Página no encontrada")