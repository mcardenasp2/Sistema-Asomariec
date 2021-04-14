from django.contrib import admin

# Register your models here.
from seguridad.models import Modulo, ModuloGrupo

admin.site.register(Modulo)
admin.site.register(ModuloGrupo)