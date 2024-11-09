from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="inicio"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('productos/', views.productos, name="productos"),
    path('contacto/', views.contacto, name="contacto"),
]