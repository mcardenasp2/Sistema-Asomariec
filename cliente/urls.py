from django.urls import path

from cliente.views import *

app_name = 'cliente'

urlpatterns = [
    # caegory
    path('cliente/mostrar/', ClienteListarView.as_view(), name='cliente_listar'),
    path('cliente/crear/', ClienteCrearView.as_view(), name='cliente_crear'),
    path('cliente/editar/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('cliente/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_eliminar'),
    # path('categoria/mostrar/', CategoriaListView.as_view(), name='categoria_mostrar'),
    # path('categoria/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
    # path('categoria/borrar/<int:pk>/', CategoriaDelete.as_view(), name='categoria_delete'),
    # path('mostrar/', mostrar, name='insumo_list'),

]