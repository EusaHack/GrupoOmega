from django.urls import path
from . import views
from .views import *


urlpatterns = [
    #path('', views.index, name="inicio"),
    path('', index.as_view(), name="inicio"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('productos/', productos.as_view(), name="productos"),
    path('contacto/', contacto.as_view(), name="contacto"),
]