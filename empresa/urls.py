from django.urls import path

from empresa.views import *

app_name = 'empresa'

urlpatterns = [
    # caegory
    path('mostrar/', EmpresaListarView.as_view(), name='empresa_listar'),
    # path('cliente/crear/', ClienteCrearView.as_view(), name='cliente_crear'),
    path('editar/<int:pk>/', EmpresaUpdateView.as_view(), name='empresa_editar'),


]