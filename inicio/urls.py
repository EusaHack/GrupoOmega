from django.urls import path
from . import views
from .views import *


urlpatterns = [
    #path('', views.index, name="inicio"),
    path('', index.as_view(), name="inicio"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('productos/', views.productos, name="productos"),
    path('contacto/', views.contacto, name="contacto"),
]