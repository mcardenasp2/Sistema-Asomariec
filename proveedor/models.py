from django.db import models
from datetime import datetime
from django.forms import model_to_dict
# Create your models here.
from Sistema_Asomariec.models import BaseModel
from crum import get_current_user

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


class Proveedor(BaseModel):
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)
    proEmpresa = models.CharField(max_length=80, verbose_name='Empresa')
    proRuc= models.CharField(max_length=13, verbose_name='Ruc')
    proDireccion = models.CharField(max_length=80, verbose_name='Direccion')
    proDescripcion = models.CharField(max_length=200,null=True, verbose_name='Descripcion')
    proTelefono = models.CharField(max_length=25,blank=True, verbose_name='Telefono')
    proEmail = models.EmailField(max_length=80, verbose_name='Email')
    proEstado = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.proEmpresa

    def get_full_name(self):
        return '{} / {}'.format(self.proEmpresa, self.proRuc)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Proveedor,self).save()

    def toJSON(self):
        item=model_to_dict(self)
        item['full_name']=self.get_full_name()
        item['provincia']= self.provincia.toJSON()
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']


