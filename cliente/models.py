from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from Sistema_Asomariec.models import BaseModel
from cliente.choices import gender_choices
from crum import get_current_user
# Create your models here.


class Cliente(BaseModel):
    cliNombre= models.CharField(max_length=150, blank=True, verbose_name='Nombre')
    cliApellido= models.CharField(max_length=150, blank=True, verbose_name='Apellido')
    cliRuc=models.CharField(max_length=13,unique=True, verbose_name='Ruc')
    cliTelefono=models.CharField(max_length=25, blank=True, verbose_name='Telefono')
    cliDireccion= models.CharField(max_length=100, blank=True, verbose_name='Direccion')
    cliGenero=models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')
    cliEmail= models.EmailField(max_length=50,blank=True,verbose_name='Email')
    cliEstado = models.BooleanField(default=True,blank=True,null=True, verbose_name='Estado')

    def __str__(self):
        # return self.cliNombre
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.cliNombre, self.cliApellido, self.cliRuc)
        # return '{} {}'.format(self.cliNombre, self.cliApellido)
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Cliente,self).save()

    def toJSON(self):
        item=model_to_dict(self)
        item['cliGenero'] = {'id': self.cliGenero, 'name': self.get_cliGenero_display()}
        item['full_name'] = self.get_full_name()
        return  item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']

class Contrato(models.Model):
    contratoDescripcion=models.CharField(max_length=150, blank=True, verbose_name='Nombre')
    cliente=models.ForeignKey(Cliente, models.PROTECT)
    contratoFec_Inicio=models.DateTimeField(default=datetime.now)
    contratoFec_Fin=models.DateTimeField(default=datetime.now)
    contratoEstado=models.BooleanField(default=True)

    def toJSON(self):
        item= model_to_dict(self)
        item['contratoFec_Inicio']=self.contratoFec_Inicio.strftime('%Y-%m-%d')
        item['contratoFec_Fin']=self.contratoFec_Fin.strftime('%Y-%m-%d')
        return item

    def __str__(self):
        self.cliente.get_full_name()

    class Meta:
        verbose_name='Contrato'
        verbose_name_plural='Contratos'
        ordering=['id']



