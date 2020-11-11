from django.urls import path

from proveedor.views import *

app_name = 'proveedor'

urlpatterns = [
    # caegory
    path('proveedor/mostrar/', ProveedorListarView.as_view(), name='proveedor_listar'),
    path('proveedor/crear/', ProveedorCrearView.as_view(), name='proveedor_crear'),
    path('proveedor/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_editar'),
    path('proveedor/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_eliminar'),
    # path('categoria/mostrar/', CategoriaListView.as_view(), name='categoria_mostrar'),
    # path('categoria/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
    # path('categoria/borrar/<int:pk>/', CategoriaDelete.as_view(), name='categoria_delete'),
    # path('mostrar/', mostrar, name='insumo_list'),

]