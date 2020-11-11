from django.urls import path

from venta.views import *

app_name = 'venta'

urlpatterns = [
    # insumo
    path('normal/mostrar/', VentaListView.as_view(), name='venta_mostrar'),
    path('normal/create/', VentaCreateView.as_view(), name='venta_create'),
    path('normal/editar/<int:pk>/', VentaUpdateView.as_view(), name='venta_edit'),
    path('normal/delete/<int:pk>/', VentaDeleteView.as_view(), name='venta_delete'),
    path('normal/delete/<int:pk>/', VentaDeleteContratoView.as_view(), name='venta_delete'),

    #     contrato
    path('contrato/create/', VentaContratoCreateView.as_view(), name='ventacont_create'),
    path('contrato/mostrar/', VentaContratoListView.as_view(), name='ventac_mostrar'),
    path('contrato/editar/<int:pk>/', VentaContratoUpdateView.as_view(), name='ventac_edit'),
    path('contrato/eliminar/<int:pk>/', VentaDeleteContratoView.as_view(), name='ventac_delete'),
]
