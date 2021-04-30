from django.db import models

from Sistema_Asomariec.models import BaseModel
from Sistema_Asomariec.settings import MEDIA_URL, STATIC_URL
# from settings import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict
# Create your models here.
from datetime import datetime
from crum import get_current_user
# Create your models here.
class Categoria(BaseModel):
    catDescripcion=models.CharField(max_length=50, verbose_name='Descripcion')
    catEstado = models.BooleanField(default=True, verbose_name='Estado')
    # usuaReg = models.IntegerField(blank=True, null=True)
    # usuaMod = models.IntegerField(blank=True, null=True)
    # usuaEli = models.IntegerField(blank=True, null=True)
    # catFecReg=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # catFecMod=models.DateTimeField(auto_now=True, blank=True, null=True)
    # catFecEli=models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return self.catDescripcion

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Categoria,self).save()

    def toJSON(self):
        item= model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class UnidadMedidad(BaseModel):
    medDescripcion=models.CharField(max_length=50,verbose_name='Medidad')
    medEstado = models.BooleanField(default=True, verbose_name='Estado')
    # usuaReg = models.IntegerField(blank=True, null=True)
    # usuaMod = models.IntegerField(blank=True, null=True)
    # usuaEli = models.IntegerField(blank=True, null=True)
    # medFecReg = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # medFecMod = models.DateTimeField(auto_now=True, blank=True, null=True)
    # medFecEli = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return self.medDescripcion

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(UnidadMedidad,self).save()

    def toJSON(self):
        item= model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Medida'
        verbose_name_plural = 'Medidas'
        ordering = ['id']


class Insumo(BaseModel):
    medida=models.ForeignKey(UnidadMedidad,on_delete=models.PROTECT)
    categoria=models.ForeignKey(Categoria, on_delete=models.PROTECT)
    insCod=models.CharField(max_length=100)
    insDescripcion=models.CharField(max_length=50, verbose_name='Descripcion')
    insModelo=models.CharField(max_length=50, verbose_name='Modelo')
    insPrecio=models.DecimalField(default=0,max_digits=10,decimal_places=2)
    # insIva=models.DecimalField(default=0,max_digits=10,decimal_places=2)
    insImagen = models.ImageField(upload_to='fotos/%Y/%m/%d', blank=True, null=True)
    insStock=models.IntegerField(default=0, blank=True, null=True,verbose_name='Stock')
    insEstado = models.BooleanField(default=True, verbose_name='Estado')
    # usuaReg = models.IntegerField(blank=True, null=True)
    # usuaMod = models.IntegerField(blank=True, null=True)
    # usuaEli = models.IntegerField(blank=True, null=True)
    # insFecReg = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # insFecMod = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.insDescripcion

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Insumo,self).save()

    def toJSON(self):
        item= model_to_dict(self)
        item['medida']=self.medida.toJSON()
        item['insImagen'] = self.get_image()
        item['categoria']= self.categoria.toJSON()
        return item

    def get_image(self):
        if self.insImagen:
            return '{}{}'.format(MEDIA_URL, self.insImagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'
        ordering = ['id']
