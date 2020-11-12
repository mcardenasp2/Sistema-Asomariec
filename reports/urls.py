from django.urls import path

from reports.views import ReportCompraView,ReportVentaView
app_name = 'reports'
urlpatterns = [
    # reports
    path('compra/', ReportCompraView.as_view(), name='compra_report'),
    path('venta/', ReportVentaView.as_view(), name='venta_report'),
]