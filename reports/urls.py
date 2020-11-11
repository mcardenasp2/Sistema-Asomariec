from django.urls import path

from reports.views import ReportCompraView
app_name = 'reports'
urlpatterns = [
    # reports
    path('compra/', ReportCompraView.as_view(), name='compra_report'),
]