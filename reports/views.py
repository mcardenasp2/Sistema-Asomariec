from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from compra.models import CabCompra
from reports.forms import ReportForm
from venta.models import Venta


class ReportCompraView(LoginRequiredMixin,TemplateView):
    template_name = 'reports/ReportCompra.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                print('hello')
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search =CabCompra.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(ccoFecCom__range=[start_date, end_date])
                print('si')
                for s in search:
                    data.append([
                        s.id,
                        s.proveedor.proEmpresa,
                        s.ccoFecCom.strftime('%Y-%m-%d'),
                        format(s.ccoSubtotal, '.2f'),
                        format(s.ccoIva, '.2f'),
                        format(s.ccoTotal, '.2f'),
                    ])

                subtotal = search.aggregate(r=Coalesce(Sum('ccoSubtotal'), 0)).get('r')
                iva = search.aggregate(r=Coalesce(Sum('ccoIva'), 0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('ccoTotal'), 0)).get('r')
                #
                data.append([
                    '---',
                    '---',
                    '---',
                    format(subtotal, '.2f'),
                    format(iva, '.2f'),
                    format(total, '.2f'),
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Reporte de Ventas'
        # context['entity'] = 'Reportes'
        # context['list_url'] = reverse_lazy('sale_report')
        context['form'] = ReportForm()
        return context

class ReportVentaView(LoginRequiredMixin,TemplateView):
    template_name = 'reports/ReportVenta.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search =Venta.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(venFechaInici__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.cliente.cliNombre,
                        s.venFechaInici.strftime('%Y-%m-%d'),
                        format(s.ventTotal, '.2f'),
                        format(s.ventTotal, '.2f'),
                        format(s.ventTotal, '.2f'),
                    ])

                subtotal = search.aggregate(r=Coalesce(Sum('ventTotal'), 0)).get('r')
                iva = search.aggregate(r=Coalesce(Sum('ventTotal'), 0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('ventTotal'), 0)).get('r')
                #
                data.append([
                    '---',
                    '---',
                    '---',
                    format(subtotal, '.2f'),
                    format(iva, '.2f'),
                    format(total, '.2f'),
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Reporte de Ventas'
        # context['entity'] = 'Reportes'
        # context['list_url'] = reverse_lazy('sale_report')
        context['form'] = ReportForm()
        return context
