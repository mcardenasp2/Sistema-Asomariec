from django.db import models
from django.forms import model_to_dict

# Create your models here.
class Empresa(models.Model):
    emprNombre = models.CharField(max_length=150, blank=True, verbose_name='Nombre')
    emprRuc=models.CharField(max_length=13,unique=True, verbose_name='Ruc')
    emprEmail = models.EmailField(max_length=50, blank=True, verbose_name='Email')
    emprTelefono = models.CharField(max_length=25, blank=True, verbose_name='Telefono')
    emprDireccion= models.CharField(max_length=100, blank=True, verbose_name='Direccion')

    def __str__(self):
        return  self.emprNombre

    def toJSON(self):
        item=model_to_dict(self)
        return  item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['id']
