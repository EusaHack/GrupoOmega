from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('hola/', views.prueba_mensaje, name="index_saludo"),
    path('create_user/', views.create_new_user, name="create_new_user"),
    path('authorization/', views.authorization, name="authorization"),
    path('auth/', views.authorizationUser, name="authorizationUser"),
    path('register/', views.codeUserValidation, name="codeUserValidation"),
    path('user_dashboard/', views.usuario_dashboard, name="user_dashboard"),
    path('dashboard/', usuario_dashboard_admin.as_view(), name='usuario_dashboard_admin'),
    path('dashboard_inicio/', DashBoardView.as_view(), name='dashboard_inicio'),
    path('modificaciones/', ModifView.as_view(), name='modificaciones'),
    path('reset/', views.reset_password, name="reset_password"),
    path('ResetPassword/', views.validar_numero, name="validar_numero"),
    path('change_password/', views.change_password, name="change_password"),
    path('logout/', views.salir, name="salir"),
]
