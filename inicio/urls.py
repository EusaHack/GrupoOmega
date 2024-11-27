from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index.as_view(), name="inicio"),
    path('nosotros/', nosotros.as_view(), name="nosotros"),
    path('productos/', productos.as_view(), name="productos"),
    path('contacto/', contacto.as_view(), name="contacto"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)