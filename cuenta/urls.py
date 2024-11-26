from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('hola/', views.prueba_mensaje, name="index_saludo"),
    path('create_user/', views.create_new_user, name="create_new_user"),
    path('authorization/', views.authorization, name="authorization"),
    path('auth/', views.authorizationUser, name="authorizationUser"),
    path('register/', views.codeUserValidation, name="codeUserValidation"),
    path('user_dashboard/', views.usuario_dashboard, name="user_dashboard"),
    path('dashboard_user/', usuario_dashboard_no_admin.as_view(), name="user_dashboard_user"),
    path('orders_user/', usuario_pedidos.as_view(), name="orders_user"),
    path('perfil_user/', usuario_perfil.as_view(), name="perfil_user"),
    path('dashboard/', usuario_dashboard_admin.as_view(), name='usuario_dashboard_admin'),
    path('dashboard_inicio/', DashBoardView.as_view(), name='dashboard_inicio'),
    path('productos_admin/', ProductosView.as_view(), name='productos_admin'),
    path('pedidos_admin/', PedidosView.as_view(), name='pedidos_admin'),
    path('usuarios_admin/', ModificacionesUsuariosVista.as_view(), name = 'usuarios_admin' ),
    path('eliminar_producto/<int:pk>/', ProductosView.as_view(), name='eliminar_producto'),
    path('modificaciones/', ModifView.as_view(), name='modificaciones'),
    path('reset/', views.reset_password, name="reset_password"),
    path('ResetPassword/', views.validar_numero, name="validar_numero"),
    path('change_password/', views.change_password, name="change_password"),
    path('logout/', views.salir, name="salir"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
