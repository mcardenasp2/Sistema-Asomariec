from django.urls import path

from producto.views import *

app_name = 'producto'

urlpatterns = [
    # insumo
    path('producto/mostrar/', ProductoListView.as_view(), name='producto_mostrar'),
    path('producto/create/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_edit'),
    path('producto/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),

]
