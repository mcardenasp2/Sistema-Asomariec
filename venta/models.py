from datetime import datetime

from django.db import models

# Create your models here.
from django.forms import model_to_dict

from producto.models import Producto
from cliente.models import Cliente
from venta.tipventa import vent_choices, vent_estado


class Venta(models.Model):
    cliente=models.ForeignKey(Cliente, on_delete=models.PROTECT)
    ventnum=models.CharField(max_length=20)
    venFechaInici=models.DateTimeField(default=datetime.now())
    venFechaFin=models.DateTimeField(default=datetime.now(),blank=True, null=True)
    ventObservacion=models.CharField(max_length=100)
    venTipo=models.CharField(max_length=20, choices=vent_choices, default='2')
    #  pendiente, pagado
    venEstVenta=models.CharField(max_length=20, choices=vent_estado, default='2')
    ventTotal=models.DecimalField(default=0.00,max_digits=9, decimal_places=2)
    ventSubtotal=models.DecimalField(default=0.00,max_digits=9, decimal_places=2)
    ventImpuesto=models.DecimalField(default=0.00,max_digits=9, decimal_places=2)
    ventEstado = models.BooleanField(default=True)

    def __str__(self):
        return self.cliente.cliNombre

    def toJSON(self):
        item= model_to_dict(self)
        item['cliente']=self.cliente.toJSON()
        item['ventTotal']=format(self.ventTotal, '.2f')
        item['ventSubtotal']=format(self.ventSubtotal, '.2f')
        item['ventImpuesto']=format(self.ventImpuesto, '.2f')
        item['venFechaInici']=self.venFechaInici.strftime('%Y-%m-%d')
        item['venFechaFin']=self.venFechaFin.strftime('%Y-%m-%d')
        item['nfact']=format(str(self.id).zfill(10))
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

