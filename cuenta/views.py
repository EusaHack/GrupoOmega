from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.contrib.auth import logout,get_user_model,login
from . import functions_x
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.http import JsonResponse
import json 
from .models import *
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
    
'''class ModifView(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/admin-m.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagina = Pagina.objects.first()
        pagina_nosotros = PaginaNosotros.objects.first()
        context['form'] = PaginaForm(instance=pagina)
        context['form_nosotros'] = PaginaFormNosotros(instance=pagina_nosotros)
        return context
    
    def post(self, request, *args, **kwargs):
        pagina = Pagina.objects.first()  # Obtener el primer objeto Pagina
        action = request.POST.get('action', 'save')  # Identificar si es guardar o restaurar
        
        if action == 'restore':
            # Restaurar datos desde la sesión
            backup_data = request.session.get('backup_data', {})
            
            if backup_data:
                # Aplicar los datos respaldados al objeto
                for field, value in backup_data.items():
                    if field == 'imagen_inicio':
                        value = value.replace("/media", "")
                    setattr(pagina, field, value)
                pagina.save()
                messages.success(request, "Datos restaurados correctamente")
            else:
                messages.error(request, "No hay datos anteriores para restaurar")
            
            return redirect('modificaciones')  # Redirigir al mismo lugar

        elif action == 'save':
            # Respaldar los datos actuales antes de guardar
            request.session['backup_data'] = {
                'titulo': pagina.titulo,
                'titulo_dos': pagina.titulo_dos,
                'color_letra_titulo': pagina.color_letra_titulo,
                'color_letra_titulo_dos': pagina.color_letra_titulo_dos,
                'color_boton': pagina.color_boton,
                'color_letra_boton': pagina.color_letra_boton,
                'imagen_inicio': pagina.imagen_inicio.url if pagina.imagen_inicio else None  # Respaldar la URL de la imagen si existe
            }

            form = PaginaForm(request.POST, request.FILES, instance=pagina)  # Procesar los datos del formulario y los archivos
            if form.is_valid():
                form.save()  # Guardar los cambios
                messages.success(request, "Datos actualizados correctamente")
                return redirect('modificaciones')  # Redirigir al mismo lugar
            
            # Si el formulario no es válido, mostrar errores
            return render(request, self.template_name, {'form': form})'''


class ModifView(LoginRequiredMixin, TemplateView):
    template_name = 'cuenta/admin-m.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagina = Pagina.objects.first()
        pagina_nosotros = PaginaNosotros.objects.first()
        pagina_productos = PaginaProductos.objects.first()
        pagina_contacto = PaginaContacto.objects.first()
        context['form'] = PaginaForm(instance=pagina)
        context['form_nosotros'] = PaginaFormNosotros(instance=pagina_nosotros)
        context['form_productos'] = PaginaFormProductos(instance=pagina_productos)
        context['form_contacto'] = PaginaFormContacto(instance=pagina_contacto)
        return context

    def post(self, request, *args, **kwargs):
        form_name = request.POST.get('form_name')
        action = request.POST.get('action', 'save')

        if form_name == 'form_principal':
            # Procesar el formulario principal
            pagina = Pagina.objects.first()
            if action == 'restore':
                backup_data = request.session.get('backup_data_principal', {})
                if backup_data:
                    for field, value in backup_data.items():
                        if field == 'imagen_inicio':
                            value = value.replace("/media", "")
                        setattr(pagina, field, value)
                    pagina.save()
                    messages.success(request, "Datos del formulario principal restaurados correctamente")
                else:
                    messages.error(request, "No hay datos anteriores para restaurar en el formulario principal")
                return redirect('modificaciones')

            elif action == 'save':
                request.session['backup_data_principal'] = {
                    'titulo': pagina.titulo,
                    'titulo_dos': pagina.titulo_dos,
                    'color_letra_titulo': pagina.color_letra_titulo,
                    'color_letra_titulo_dos': pagina.color_letra_titulo_dos,
                    'color_boton': pagina.color_boton,
                    'color_letra_boton': pagina.color_letra_boton,
                    'imagen_inicio': pagina.imagen_inicio.url if pagina.imagen_inicio else None
                }
                form = PaginaForm(request.POST, request.FILES, instance=pagina)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Datos del formulario principal actualizados correctamente")
                return redirect('modificaciones')

        elif form_name == 'form_productos':
            # Procesar el formulario de "Nosotros"
            pagina_productos = PaginaProductos.objects.first()
            if action == 'restore':
                backup_data = request.session.get('backup_data_productos', {})
                if backup_data:
                    for field, value in backup_data.items():
                        setattr(pagina_productos, field, value)
                    pagina_productos.save()
                    messages.success(request, "Datos del formulario 'Nosotros' restaurados correctamente")
                else:
                    messages.error(request, "No hay datos anteriores para restaurar en el formulario 'Nosotros'")
                return redirect('modificaciones')

            elif action == 'save':
                request.session['backup_data_productos'] = {
                    'color_letra_titulo': pagina_productos.color_letra_titulo,
                    'color_letra_titulo_dos': pagina_productos.color_letra_titulo_dos,
                    'color_btn': pagina_productos.color_btn,
                    'color_letra_btn': pagina_productos.color_letra_btn,
                }
                form_productos = PaginaFormProductos(request.POST, instance=pagina_productos)
                if form_productos.is_valid():
                    form_productos.save()
                    messages.success(request, "Datos del formulario 'Nosotros' actualizados correctamente")
                return redirect('modificaciones')
            
        elif form_name == 'form_contacto':
            # Procesar el formulario de "Nosotros"
            pagina_contacto = PaginaContacto.objects.first()
            if action == 'restore':
                backup_data = request.session.get('backup_data_contacto', {})
                if backup_data:
                    for field, value in backup_data.items():
                        setattr(pagina_contacto, field, value)
                    pagina_contacto.save()
                    messages.success(request, "Datos del formulario 'Nosotros' restaurados correctamente")
                else:
                    messages.error(request, "No hay datos anteriores para restaurar en el formulario 'Nosotros'")
                return redirect('modificaciones')

            elif action == 'save':
                request.session['backup_data_contacto'] = {
                    'color_letra_titulo': pagina_contacto.color_letra_titulo,
                    'color_letra_titulo_dos': pagina_contacto.color_letra_titulo_dos,
                    'color_btn': pagina_contacto.color_btn,
                    'color_letra_btn': pagina_contacto.color_letra_btn,
                }
                form_contacto = PaginaFormContacto(request.POST, instance=pagina_contacto)
                if form_contacto.is_valid():
                    form_contacto.save()
                    messages.success(request, "Datos del formulario 'Nosotros' actualizados correctamente")
                return redirect('modificaciones')
            
        elif form_name == 'form_nosotros':
            # Procesar el formulario de "Nosotros"
            pagina_nosotros = PaginaNosotros.objects.first()
            if action == 'restore':
                backup_data = request.session.get('backup_data_nosotros', {})
                if backup_data:
                    for field, value in backup_data.items():
                        setattr(pagina_nosotros, field, value)
                    pagina_nosotros.save()
                    messages.success(request, "Datos del formulario 'Nosotros' restaurados correctamente")
                else:
                    messages.error(request, "No hay datos anteriores para restaurar en el formulario 'Nosotros'")
                return redirect('modificaciones')

            elif action == 'save':
                request.session['backup_data_nosotros'] = {
                    'titulo': pagina_nosotros.titulo,
                    'titulo_dos': pagina_nosotros.titulo_dos,
                    'color_letra_titulo': pagina_nosotros.color_letra_titulo,
                    'color_letra_titulo_dos': pagina_nosotros.color_letra_titulo_dos,
                    'txt_uno': pagina_nosotros.txt_uno,
                    'txt_dos': pagina_nosotros.txt_dos,
                    'color_txt_uno': pagina_nosotros.color_txt_uno,
                    'color_txt_dos': pagina_nosotros.color_txt_dos,
                }
                form_nosotros = PaginaFormNosotros(request.POST, instance=pagina_nosotros)
                if form_nosotros.is_valid():
                    form_nosotros.save()
                    messages.success(request, "Datos del formulario 'Nosotros' actualizados correctamente")
                return redirect('modificaciones')

        # Si no se identifica el formulario, redirigir
        messages.error(request, "Formulario no identificado")
        return redirect('modificaciones')

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