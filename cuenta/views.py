from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.contrib.auth import logout,get_user_model,login
from .models import CustomUser
from . import functions_x
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

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
        return render(request, 'cuenta/user.html')

class usuario_dashboard_admin(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/admin.html'

class DashBoardView(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/admin-d.html'
    
class ModifView(LoginRequiredMixin,TemplateView):
    template_name = 'cuenta/admin-m.html'

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