from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from django_countries.fields import CountryField # esta libreria me sirve para los PAISES





# Create your models here.
class PaqueteTuristico(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    incluye = models.TextField()
    no_incluye = models.TextField()
    imagenUno = models.ImageField(upload_to='imagenes/', null=True)
    imagenDos = models.ImageField(upload_to='imagenes/', null=True)
    imagenTres = models.ImageField(upload_to='imagenes/', null=True)
    def __str__(self):
        return self.nombre

class FechasReserva(models.Model):
    paquete = models.ForeignKey(PaqueteTuristico, null=False, blank=False, on_delete=models.CASCADE)
    fechaInicio = models.DateField()
    fechaFinal = models.DateField()
    personas = models.IntegerField(default=0)

def clean(self):
        if self.personas < 1:
            raise ValidationError('El número de personas debe ser al menos 1.')    
def __str__(self):
    return 
    self.fechaInicio+''+self.fechaFinal+''+self.personas

class Cliente(models.Model):
    paquete = models.ForeignKey(PaqueteTuristico, on_delete=models.SET_NULL,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=False)
    TIPO_DOCUMENTO_CHOICES = [
        ('Cédula', 'Cédula de Ciudadanía'),
        ('Cédula_Extranjeria', 'Cédula de Extranjeria'),
        ('Tarjeta_Extranjería', 'Tarjeta de Extranjería'),
        ('Pasaporte', 'Pasaporte'),
    ]
    tipo_documento = models.CharField(max_length=30, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField(max_length=30)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    nacionalidad = CountryField(blank_label='Seleccione un país')  # Cambiado a CountryField
    fecha_registro = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.email} - {self.get_nacionalidad_display()}"
   




   

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, null=False, blank=False, on_delete=models.CASCADE)
    paquete = models.ForeignKey(PaqueteTuristico, null=False, blank=False, on_delete=models.CASCADE)
    fecha_reserva = models.ForeignKey(FechasReserva, null=False, blank=False,on_delete=models.CASCADE)
    fechaReserva = models.DateField(auto_now_add=True)
    horaReserva = models.TimeField(auto_now_add=True)
    def __str__(self): 
        fecha_formateada = self.fechaReserva.strftime("%d %B %Y")
        hora_formateada = self.horaReserva.strftime("%H:%M:%S")
        return f'{self.cliente} {self.paquete} {fecha_formateada} {hora_formateada}'
   

   
    





