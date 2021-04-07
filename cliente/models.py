from datetime import datetime
from django.db import models
from django.forms import model_to_dict
from cliente.choices import gender_choices

# Create your models here.


class Cliente(models.Model):
    cliNombre= models.CharField(max_length=150, blank=True, verbose_name='Nombre')
    cliApellido= models.CharField(max_length=150, blank=True, verbose_name='Apellido')
    cliRuc=models.CharField(max_length=13,unique=True, verbose_name='Ruc')
    cliTelefono=models.CharField(max_length=25, blank=True, verbose_name='Telefono')
    cliDireccion= models.CharField(max_length=100, blank=True, verbose_name='Direccion')
    cliGenero=models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')
    cliEmail= models.EmailField(max_length=50,blank=True,verbose_name='Email')
    cliEstado = models.BooleanField(default=True,blank=True,null=True, verbose_name='Estado')
    usuaReg=models.IntegerField(blank=True, null=True)
    cliFecReg=models.DateTimeField(auto_now_add=True,blank=True, null=True)
    usuaMod = models.IntegerField(blank=True, null=True)
    cliFecMod = models.DateTimeField(auto_now=True,blank=True, null=True)
    usuaEli = models.IntegerField(blank=True, null=True)
    # cliFecEli = models.DateTimeField(default=datetime.now(), blank=True, null=True)

    def __str__(self):
        # return self.cliNombre
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.cliNombre, self.cliApellido, self.cliRuc)
        # return '{} {}'.format(self.cliNombre, self.cliApellido)

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



