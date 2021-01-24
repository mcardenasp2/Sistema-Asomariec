from django.urls import path

from producto.views import *

app_name = 'producto'

urlpatterns = [
    # insumo
    path('producto/mostrar/', ProductoListView.as_view(), name='producto_mostrar'),
    path('producto/create/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_edit'),
    path('producto/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),

    #     product
    path('product/mostrar/', ProductListView.as_view(), name='product_mostrar'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/editar/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/eliminar/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

]
