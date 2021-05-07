from django.urls import path

from venta.views import *

app_name = 'venta'

urlpatterns = [
    # Venta
    path('normal/mostrar/', VentaListView.as_view(), name='venta_mostrar'),
    path('normal/create/', VentaCreateView.as_view(), name='venta_create'),
    # path('normal/editar/<int:pk>/', VentaUpdateView.as_view(), name='venta_edit'),
    path('normal/eliminar/', VentaDelete.as_view(), name='venta_delete'),
    # path('normal/delete/<int:pk>/', VentaDeleteView.as_view(), name='venta_delete'),
    # path('normal/delete/<int:pk>/', VentaDeleteContratoView.as_view(), name='venta_delete'),
    path('normal/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='venta_invoice_pdf'),

    #     contrato
    path('contrato/create/', VentaContratoCreateView.as_view(), name='ventacont_create'),
    path('contrato/mostrar/', VentaContratoListView.as_view(), name='ventac_mostrar'),
    path('contrato/eliminar/', VentaContratoDelete.as_view(), name='ventac_eliminar'),
    # path('contrato/editar/<int:pk>/', VentaContratoUpdateView.as_view(), name='ventac_edit'),
    # Detalle del COntrato
    path('contrato/detalle/<int:pk>/', VentaContratoDetalleView.as_view(), name='ventac_detalle'),

    # path('contrato/eliminar/<int:pk>/', VentaDeleteContratoView.as_view(), name='ventac_delete'),
    path('contrato/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='ventac_invoice_pdf'),
]
