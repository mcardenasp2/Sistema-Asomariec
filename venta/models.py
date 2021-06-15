from datetime import datetime

from django.db import models

# Create your models here.
from django.forms import model_to_dict

from user.models import User

from Sistema_Asomariec.models import BaseModel
from producto.models import Producto
from cliente.models import Cliente
from venta.tipventa import vent_choices, vent_estado
from crum import get_current_user

class Venta(BaseModel):
    cliente=models.ForeignKey(Cliente, on_delete=models.PROTECT)
    ventnum=models.CharField(max_length=20)
    venFechaInici=models.DateField(default=datetime.now)
    venFechaFin=models.DateField(default=datetime.now,blank=True, null=True)
    ventDescuento=models.DecimalField(default=0.00,max_digits=9, decimal_places=2)
    ventTotalDescuento=models.DecimalField(default=0.00,max_digits=9, decimal_places=2)
    ventObservacion=models.CharField(max_length=100)
    venTipo=models.CharField(max_length=20, choices=vent_choices, default='2')
    #  pendiente, pagado
    venEstVenta=models.CharField(max_length=20, choices=vent_estado, default='1')
    ventTotal=models.DecimalField(default=0.00,max_digits=9, decimal_places=2)
    ventSubtotal=models.DecimalField(default=0.00,max_digits=9, decimal_places=2)
    ventImpuesto=models.DecimalField(default=0.00,max_digits=9, decimal_places=2)
    ventEstado = models.BooleanField(default=True)

    def __str__(self):
        return self.cliente.cliNombre

    def get_full_name_usuario(self):
        # usr= User.objects.get(pk=self.user_creation).toJSON()
        usr= User.objects.get(pk=self.user_creation_id).toJSON()
        return usr['full_name']

        # return '{} {} / {}'.format(self.user_creation, self.cliApellido, self.cliRuc)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Venta,self).save()

    def toJSON(self):
        item= model_to_dict(self)
        item['cliente']=self.cliente.toJSON()
        item['ventTotal']=format(self.ventTotal, '.2f')
        item['ventSubtotal']=format(self.ventSubtotal, '.2f')
        item['ventDescuento']=format(self.ventDescuento, '.2f')
        item['ventImpuesto']=format(self.ventImpuesto, '.2f')
        item['venFechaInici']=self.venFechaInici.strftime('%Y-%m-%d')
        item['venFechaFin']=self.venFechaFin.strftime('%Y-%m-%d')
        item['nfact']=format(str(self.id).zfill(10))
        item['ventusuario']=self.get_full_name_usuario()
        return item

    class Meta:
        verbose_name='Venta'
        verbose_name_plural= 'Ventas'
        ordering=['id']


class DetVenta(models.Model):
    venta=models.ForeignKey(Venta, on_delete=models.PROTECT)
    producto=models.ForeignKey(Producto, on_delete=models.PROTECT)
    detPrecio=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    detCant= models.IntegerField(default=1)
    detSubtotal=models.DecimalField(default=0,max_digits=10,decimal_places=2)

    def __str__(self):
        return self.producto.prodDescripcion

    def toJSON(self):
        item=model_to_dict(self,exclude=['venta'])
        item['producto']=self.producto.toJSON()
        item['detPrecio'] = format(self.detPrecio, '.2f')
        item['detSubtotal'] = format(self.detSubtotal, '.2f')
        return item


class GastAdc(models.Model):
    venta=models.ForeignKey(Venta, on_delete=models.PROTECT)
    gastdescripcion = models.CharField(max_length=100)
    gastprecio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.gastdescripcion

    def toJSON(self):
        item=model_to_dict(self, exclude=['venta'])
        item['gastprecio'] = format(self.gastprecio, '.2f')
        return item

    class Meta:
        verbose_name='Detalle de Venta'
        verbose_name_plural='Detalle de Ventas'
        ordering = ['id']

class Contrato(models.Model):
    cabventa=models.ForeignKey(Venta, on_delete=models.PROTECT)
    ctrnombre=models.CharField(max_length=150, blank=True, verbose_name='Nombre')
    ctrFec_Inicio=models.DateTimeField(default=datetime.now)
    ctrFec_Fin=models.DateTimeField(default=datetime.now)
    ctrEstado=models.BooleanField(default=True)

    def toJSON(self):
        item= model_to_dict(self)
        item['ctrFec_Inicio']=self.ctrFec_Inicio.strftime('%Y-%m-%d')
        item['ctrFec_Fin']=self.ctrFec_Fin.strftime('%Y-%m-%d')
        return item

    def __str__(self):
        self.cabventa.cliente.get_full_name()
    #
    class Meta:
        verbose_name='Contrato'
        verbose_name_plural='Contratos'
        ordering=['id']

