from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, number, name_business, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, number=number, name_business=name_business, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, number, name_business, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, number, name_business, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    name_business = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    number = models.CharField(max_length=10)
    password = models.CharField(max_length=200)
    last_login = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'number', 'name_business']

    def __str__(self):
        return self.email


# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre
    
# Modelo de Pedido
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('entregado', 'Entregado'),
        ('en progreso', 'En Progreso'),
        ('cancelado', 'Cancelado')
    ]
    
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado_entrega = models.CharField(
        max_length=11, choices=ESTADO_CHOICES, default='pendiente'
    )
    razon_cancelacion = models.TextField(blank=True, null=True)
    confirmacion_entrega = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido de {self.usuario.username} para {self.producto.nombre}"

    def total(self):
        return self.cantidad * self.producto.precio


class Pagina(models.Model):
    titulo = models.CharField(max_length=500, default="Empaqueta tu futuro con nuestras cajas multiusos...")
    titulo_dos = models.CharField(max_length=500, default="¡DESCUBRE LA CALIDAD QUE MARCA LA DIFERENCA!")
    color_letra_titulo = models.CharField(max_length=8, default="#2b4e71")
    color_letra_titulo_dos = models.CharField(max_length=8, default="#ffffff")
    color_boton = models.CharField(max_length=8, default="#2b4e71")
    color_letra_boton = models.CharField(max_length=8, default="#ffff")
    imagen_inicio = models.ImageField(upload_to='inicio/images/', blank=True, null=True)  # campo para la imagen

    def __str__(self):
        return 'index'
    
    
class PaginaNosotros(models.Model):
    titulo = models.CharField(max_length=100, default="¿Quiénes somos?")
    titulo_dos = models.CharField(max_length=500, default="Diferencias")
    color_letra_titulo = models.CharField(max_length=8, default="#2b4e71")
    color_letra_titulo_dos = models.CharField(max_length=8, default="#ffffff")
    txt_uno = models.TextField(default="") 
    txt_dos = models.TextField(default="")
    color_txt_uno = models.CharField(max_length=8, default="#2b4e71")
    color_txt_dos = models.CharField(max_length=8, default="#ffffff")

    def __str__(self):
        return 'Nosotros'
    

class PaginaProductos(models.Model):
    color_letra_titulo = models.CharField(max_length=8, default="#2b4e71")
    color_letra_titulo_dos = models.CharField(max_length=8, default="#ffffff")
    color_btn = models.CharField(max_length=8, default="#2b4e71")
    color_letra_btn = models.CharField(max_length=8, default="#ffffff")

    def __str__(self):
        return 'Productos'
    
class PaginaContacto(models.Model):
    color_letra_titulo = models.CharField(max_length=8, default="#2b4e71")
    color_letra_titulo_dos = models.CharField(max_length=8, default="#ffffff")
    color_btn = models.CharField(max_length=8, default="#2b4e71")
    color_letra_btn = models.CharField(max_length=8, default="#ffffff")

    def __str__(self):
        return 'Contacto'