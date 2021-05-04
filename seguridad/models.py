from django.db import models
from django.contrib.auth.models import User, Group
from django.forms import model_to_dict

# Create your models here.
class Modulo(models.Model):
    url = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.nombre)

    def toJSON(self):
        item=model_to_dict(self)
        return  item

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['orden']

class ModuloGrupo(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True)
    modulos = models.ManyToManyField(Modulo)
    grupos = models.ManyToManyField(Group)
    prioridad = models.IntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def toJSON(self):
        item=model_to_dict(self)
        item['grupos'] = [{'id': g.id, 'nombre': g.name} for g in self.grupos.all()]
        item['modulos'] = [{'id': g.id, 'nombre': g.nombre} for g in self.modulos.all()]
        return  item

    class Meta:
        verbose_name = 'Grupo de Módulos'
        verbose_name_plural = 'Grupos de Módulos'
        ordering = ('prioridad', 'nombre')

    def modulos_activos(self):
        return self.modulos.filter(activo=True).order_by('orden')


# class Group(Group):
#     def toJSON(self):
#         item=model_to_dict(self)
#         # item['grupos'] = [{'id': g.id, 'nombre': g.name} for g in self.grupos.all()]
#         item['permissions'] = [{'id': g.id, 'name': g.name} for g in self.permissions.all()]
#         return  item
