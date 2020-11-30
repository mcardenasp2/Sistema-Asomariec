from django.urls import path

from reports.views import ReportCompraView, ReportVentaView, SaleInvoicePdfView, VentaPdfView

app_name = 'reports'
urlpatterns = [
    # reports
    path('compra/', ReportCompraView.as_view(), name='compra_report'),
    path('venta/', ReportVentaView.as_view(), name='venta_report'),
    path('invoice/pdf/<str:start_date>&<str:end_date>/', SaleInvoicePdfView.as_view(), name='compra_invoice_pdf'),
    path('venta/pdf/<str:start_date>&<str:end_date>/', VentaPdfView.as_view(), name='venta_pdf'),
    # path('invoice/pdf/', SaleInvoicePdfView.as_view(), name='compra_invoice_pdf'),
]