from django.urls import path

from compra.views import *

app_name = 'compra'

urlpatterns = [

    # cabcompra
    path('compra/crear/', CabCompraCreateView.as_view(), name='compra_crear'),
    path('compra/mostrar/', CabComprListView.as_view(), name='compra_listar'),
    # path('compra/editar/<int:pk>/', CabCompraUpdateView.as_view(), name='compra_editar'),
    # path('compra/eliminar/<int:pk>/', CabCompraDeleteView.as_view(), name='compra_delete'),
    path('compra/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='compra_invoice_pdf'),

    # path('insumo/create/', InsumoCreateView.as_view(), name='insumo_create'),
    # path('insumo/editar/<int:pk>/', InsumoUpdateView.as_view(), name='insumo_edit'),

]
