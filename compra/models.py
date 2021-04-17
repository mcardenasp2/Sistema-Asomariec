from django.db import models

from datetime import datetime
# Create your models here.
from django.forms import model_to_dict

from Sistema_Asomariec.settings import MEDIA_URL, STATIC_URL
from proveedor.models import Proveedor
from insumo.models import Insumo
#
class CabCompra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    # comprador = models.CharField(max_length=5)
    ccoFecCom = models.DateField(default=datetime.now)
    ccoVendedor=models.CharField(max_length=50, verbose_name='Vendedor')
    ccoCedVend=models.CharField(max_length=13, verbose_name='Cedula')
    # ccoReferencia = models.CharField(max_length=20,verbose_name='Referencia')
    # plcTipPag = models.CharField(max_length=20,verbose_name='Tipo Pago')
    # plcTipCom = models.CharField(max_length=20,verbose_name='Tipo Compra')
    ccoSubtotal =models.DecimalField(default=0,max_digits=10,decimal_places=2)
    # ccoDescuento =models.DecimalField(default=0,max_digits=10,decimal_places=2)
    ccoIva = models.DecimalField(default=0,max_digits=10,decimal_places=2)
    ccoTotal = models.DecimalField(default=0,max_digits=10,decimal_places=2)
    ccoEstado = models.BooleanField(default=True, verbose_name='Estado')

    ccoDocumento=models.FileField(upload_to='documento/%Y/%m/%d', blank=True, null=True)

    usuaReg = models.IntegerField(blank=True, null=True)
    usuaMod = models.IntegerField(blank=True, null=True)
    usuaEli = models.IntegerField(blank=True, null=True)
    ccoFecReg = models.DateTimeField(default=datetime.now())
    ccoFecMod = models.DateTimeField(default=datetime.now())
    ccoFecEli = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.proveedor.proEmpresa

    def toJSON(self):
        item= model_to_dict(self)
        item['proveedor']= self.proveedor.toJSON()
        item['ccoSubtotal'] = format(self.ccoSubtotal, '.2f')
        item['ccoIva'] = format(self.ccoIva, '.2f')
        item['ccoTotal'] = format(self.ccoTotal, '.2f')
        item['ccoDocumento'] = self.get_doc()
        item['ccoFecCom'] = self.ccoFecCom.strftime('%Y-%m-%d')
        return item

    def get_doc(self):
        if self.ccoDocumento:
            return '{}{}'.format(MEDIA_URL, self.ccoDocumento)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Cabecera Compra'
        verbose_name_plural = 'Cabecera Compras'
        ordering = ['id']


class DetCompra(models.Model):
    cabCompra=models.ForeignKey(CabCompra, on_delete=models.PROTECT)
    insumo = models.ForeignKey(Insumo,on_delete=models.PROTECT)
    dcoPreCom  = models.DecimalField(default=0,max_digits=10,decimal_places=2)
    dcoCantidad = models.IntegerField(default=0)
    dcoSubtotal  = models.DecimalField(default=0,max_digits=10,decimal_places=2)

    def __str__(self):
        return self.insumo.insDescripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['cabCompra'])
        item['insumo'] = self.insumo.toJSON()
        item['dcoPreCom'] = format(self.dcoPreCom, '.2f')
        item['dcoSubtotal'] = format(self.dcoSubtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle Compra'
        verbose_name_plural = 'Detalle Compras'
        ordering = ['id']
