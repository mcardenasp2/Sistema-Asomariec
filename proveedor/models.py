from django.db import models
from datetime import datetime
from django.forms import model_to_dict
# Create your models here.

class Provincia(models.Model):
    prvDescripcion = models.CharField(max_length=50, verbose_name='Descripcion')
    prvEstado = models.BooleanField(default=True, verbose_name='Estado')
    usuaReg = models.IntegerField(blank=True, null=True)
    usuaMod = models.IntegerField(blank=True, null=True)
    usuaEli = models.IntegerField(blank=True, null=True)
    prvFecReg = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    prvFecMod = models.DateTimeField(auto_now=True, blank=True, null=True)
    # prvFecEli = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return self.prvDescripcion

    def toJSON(self):
        item=model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['id']


class Proveedor(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)
    proEmpresa = models.CharField(max_length=80, verbose_name='Empresa')
    proRuc= models.CharField(max_length=13, verbose_name='Ruc')
    proDireccion = models.CharField(max_length=80, verbose_name='Direccion')
    proDescripcion = models.CharField(max_length=200,null=True, verbose_name='Descripcion')
    proTelefono = models.CharField(max_length=25, verbose_name='Telefono')
    proEmail = models.EmailField(max_length=80, verbose_name='Email')
    proEstado = models.BooleanField(default=True, verbose_name='Estado')
    usuaReg = models.IntegerField(blank=True, null=True)
    usuaMod = models.IntegerField(blank=True, null=True)
    usuaEli = models.IntegerField(blank=True, null=True)
    proFecReg = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    proFecMod = models.DateTimeField(auto_now=True, blank=True, null=True)
    # proFecEli = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return self.proEmpresa


    def toJSON(self):
        item=model_to_dict(self)
        item['provincia']= self.provincia.toJSON()
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']


