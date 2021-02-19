from datetime import datetime
from Sistema_Asomariec.settings import MEDIA_URL, STATIC_URL
from django.db import models

from insumo.models import Insumo
# Create your models here.
from django.forms import model_to_dict


class Producto(models.Model):
    prodDescripcion = models.CharField(max_length=100, verbose_name='Descripcion')
    # prodFecElab=models.DateTimeField(default=datetime.now())
    prodImagen= models.ImageField(upload_to='producto', blank=True, null=True)
    prodImagen2= models.ImageField(upload_to='producto2', blank=True, null=True)
    prodCantidad=models.IntegerField(default=0, blank=True, null=True)
    prodPrecio=models.DecimalField(default=0,max_digits=9, decimal_places=2)
    prodTotal=models.DecimalField(default=0.00,max_digits=9, decimal_places=2,blank=True, null=True)
    prodIva = models.DecimalField(default=0.12, max_digits=10, decimal_places=2)
    # prodTalla=models.CharField(max_length=100)
    prodCaracteristica=models.TextField(max_length=400, null=True, blank=True)
    # estado de la produccion
    # 1 finalizado; 2 en proceso
    prodEstprod=models.IntegerField(default=1,blank=True)
    # referencia si es por contrato o venta normal
    # 1 contrato, 2 normal
    prodTipo=models.IntegerField(default=2,blank=True)
    prodEstado = models.BooleanField(default=True, verbose_name='Estado')
    usuaReg = models.IntegerField(blank=True, null=True)
    usuaMod = models.IntegerField(blank=True, null=True)
    usuaEli = models.IntegerField(blank=True, null=True)
    prodFecReg = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    prodFecMod = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    prodFecEli = models.DateTimeField(default=datetime.now(), blank=True, null=True)

    def __str__(self):
        return self.prodDescripcion

    def toJSON(self):
        item=model_to_dict(self)
        item['prodImagen'] = self.get_image()
        item['prodImagen2'] = self.get_image2()
        item['prodPrecioTotal'] = format((self.prodPrecio*self.prodIva)+self.prodPrecio, '.2f')
        item['prodPrecio'] = format(self.prodPrecio, '.2f')
        item['prodIva'] = format(self.prodIva, '.2f')
        item['prodTotal'] = format(self.prodTotal, '.2f')
        # item['prodFecElab'] = self.prodFecElab.strftime('%Y-%m-%d')
        return item

    def get_image(self):
        if self.prodImagen:
            return '{}{}'.format(MEDIA_URL, self.prodImagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def get_image2(self):
        if self.prodImagen2:
            return '{}{}'.format(MEDIA_URL, self.prodImagen2)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name='Producto'
        verbose_name_plural='Productos'
        ordering = ['id']


class Produccion(models.Model):
    producto=models.ForeignKey(Producto,on_delete=models.PROTECT)
    prodcFecElab = models.DateTimeField(default=datetime.now())
    prodcCantidad = models.IntegerField(default=1)
    prodcTotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    prodcEstado = models.BooleanField(default=True, verbose_name='Estado')
    # estado de la produccion
    # prodcEstprod = models.IntegerField(default=0)
    # referencia si es por contrato o venta normal
    prodcTipo = models.IntegerField(default=1)

    def __str__(self):
        return self.producto.prodDescripcion

    def toJSON(self):
        item=model_to_dict(self)
        item['producto'] = self.producto.toJSON()
        # item['prodcTotal'] = format((self.prodcTotal*self.prodIva)+self.prodPrecio, '.2f')
        item['prodcTotal'] = format(self.prodcTotal, '.2f')
        # item['prodIva'] = format(self.prodIva, '.2f')
        # item['prodTotal'] = format(self.prodTotal, '.2f')
        item['prodcFecElab'] = self.prodcFecElab.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name='Produccion'
        verbose_name_plural='Producciones'
        ordering = ['id']


class DetProducto(models.Model):
    # producto=models.ForeignKey(Producto,on_delete=models.PROTECT)
    produccion=models.ForeignKey(Produccion,on_delete=models.PROTECT)

    insumo=models.ForeignKey(Insumo,on_delete=models.PROTECT)
    # detcantidad= models.IntegerField(default=0)
    detprecio=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    detCantidad = models.IntegerField(default=1)
    detSubtotal = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.insumo.insDescripcion

    def toJSON(self):
        item= model_to_dict(self, exclude=['producto'])
        item['insumo']=self.insumo.toJSON()
        item['detprecio'] = format(self.detprecio, '.2f')
        item['detSubtotal'] = format(self.detSubtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Producto'
        verbose_name_plural = 'Detalle de Productos'
        ordering = ['id']

class GastosAdicionales(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    gastdescripcion = models.CharField(max_length=100)
    gastprecio= models.DecimalField(default=0.00,max_digits=9, decimal_places=2)

    def __str__(self):
        return self.gastdescripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['producto'])
        item['gastprecio'] = format(self.gastprecio, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle Gastos Adicional'
        verbose_name_plural = 'Detalle Gastos Adicionales'
        ordering = ['id']
