from django.urls import path

from insumo.views import *

app_name = 'insumo'

urlpatterns = [
    # category
    path('categoria/mostrar/', CategoriaView.as_view(), name='categoria_mostrar'),
    path('categoria/create/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categoria/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categoria/borrar/<int:pk>/', CategoriaDelete.as_view(), name='categoria_delete'),
    path('mostrar/', mostrar, name='insumo_list'),
    # medida
    path('medida/mostrar/', MedidaView.as_view(), name='medida_mostrar'),
    # detalle
    path('detalle/mostrar/',DetalleView.as_view(), name='detalle_mostrar'),
    # insumo
    path('insumo/mostrar/', InsumoListView.as_view(), name='insumo_mostrar'),
    path('insumo/create/', InsumoCreateView.as_view(), name='insumo_create'),
    path('insumo/editar/<int:pk>/', InsumoUpdateView.as_view(), name='insumo_edit'),
    # path('insumo/eliminar/<int:pk>/', InsumoDeleteView.as_view(), name='insumo_delete'),

]
