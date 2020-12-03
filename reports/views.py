from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
# from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from compra.models import CabCompra
from reports.forms import ReportForm
from venta.models import Venta


import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


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
                # print('hello')
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search =CabCompra.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(ccoFecCom__range=[start_date, end_date])
                # print('si')
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
                tipo = request.POST.get('tipo', '')
                # print('tipo'+tipo)
                search =Venta.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(venFechaInici__range=[start_date, end_date], ventEstado=1, venEstVenta=2)
                if len(start_date) and len(end_date) and tipo=='3':
                    #sin contrato
                    search = search.filter(venFechaInici__range=[start_date, end_date],venTipo=2, ventEstado=1, venEstVenta=2)
                if len(start_date) and len(end_date) and tipo=='2':
                    # contrto
                    search = search.filter(venFechaInici__range=[start_date, end_date],venTipo=1, ventEstado=1, venEstVenta=2)
                for s in search:
                    data.append([
                        s.id,
                        s.cliente.cliNombre,
                        s.venFechaInici.strftime('%Y-%m-%d'),
                        format(s.ventSubtotal, '.2f'),
                        format(s.ventImpuesto, '.2f'),
                        format(s.ventTotal, '.2f'),
                    ])

                subtotal = search.aggregate(r=Coalesce(Sum('ventSubtotal'), 0)).get('r')
                iva = search.aggregate(r=Coalesce(Sum('ventImpuesto'), 0)).get('r')
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



class SaleInvoicePdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # result = finders.find(uri)
        # if result:
        #     if not isinstance(result, (list, tuple)):
        #         result = [result]
        #     result = list(os.path.realpath(path) for path in result)
        #     path = result[0]
        # else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path


    def get(self, request, *args, **kwargs):
        try:
            # print('hhhhhhhhhhhhhhh')
            print(self.kwargs['start_date'])
            print(self.kwargs['end_date'])
            data = []
            start_date = self.kwargs['start_date']
            end_date = self.kwargs['end_date']
            search = CabCompra.objects.all()
            if len(start_date) and len(end_date):
                print('gggggg')
                search = search.filter(ccoFecCom__range=[start_date, end_date])
            # print('si')
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

            subtotal1= format(subtotal, '.2f')
            iva=format(iva, '.2f')
            total=format(total, '.2f')
            #
            # data.append([
            #     '---',
            #     '---',
            #     '---',
            #     format(subtotal, '.2f'),
            #     format(iva, '.2f'),
            #     format(total, '.2f'),
            # ])
            # print(data)
            # for i in data:
                # print('ffff')
                # print(i[0])


            # print(request.POST['param'])
            template = get_template('reports/invoice.html')
            # context = {'sale': CabCompra.objects.get(pk=self.kwargs['pk']),
            context = {'sale': CabCompra.objects.get(pk=1),
                       'comp': {'name': 'AlgoriSoft S.A', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                       'icon':'{}{}'.format(settings.MEDIA_URL, 'logo2.jpeg'),
                       'report':data,
                       'totales':{'subtotal':subtotal1,'iva':iva,'total':total}
                       # se utiliza con collectstatic
                       # 'icon':'{}{}'.format(settings.STATIC_URL, 'img/logo2.jpeg')

                       }
            html = template.render(context)
            # print('pdf no imprime')
            response = HttpResponse(content_type='application/pdf')
            # print('pdf no imprime nada')
            # para descargar el pdf
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback

            )
            # print('este no corrio')
            # if error then show some funy view
            # if pisa_status.err:
                # return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        except:
            print('pdf no imprime nada de nada')
            pass
        return HttpResponseRedirect(reverse_lazy('compra:compra_listar'))

class VentaPdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # result = finders.find(uri)
        # if result:
        #     if not isinstance(result, (list, tuple)):
        #         result = [result]
        #     result = list(os.path.realpath(path) for path in result)
        #     path = result[0]
        # else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path


    def get(self, request, *args, **kwargs):
        try:
            # print('hhhhhhhhhhhhhhh')
            print(self.kwargs['start_date'])
            print(self.kwargs['end_date'])

            data = []
            # start_date = request.POST.get('start_date', '')
            # end_date = request.POST.get('end_date', '')
            start_date = self.kwargs['start_date']
            end_date = self.kwargs['end_date']
            tipo = self.kwargs['tipo']
            search = Venta.objects.all()
            descr = ''
            if len(start_date) and len(end_date):
                # print('xxxxxxxxxxxxxx')
                search = search.filter(venFechaInici__range=[start_date, end_date], ventEstado=1, venEstVenta=2)

            if len(start_date) and len(end_date) and tipo == '3':
                # sin contrato
                search = search.filter(venFechaInici__range=[start_date, end_date], venTipo=2, ventEstado=1, venEstVenta=2)
                descr = 'Sin Contrato'
            if len(start_date) and len(end_date) and tipo == '2':
                # contrto
                search = search.filter(venFechaInici__range=[start_date, end_date], venTipo=1, ventEstado=1, venEstVenta=2)
                descr = 'Contrato'
            for s in search:
                data.append([
                    s.id,
                    s.cliente.cliNombre,
                    s.venFechaInici.strftime('%Y-%m-%d'),
                    format(s.ventSubtotal, '.2f'),
                    format(s.ventImpuesto, '.2f'),
                    format(s.ventTotal, '.2f'),
                ])

            subtotal = search.aggregate(r=Coalesce(Sum('ventSubtotal'), 0)).get('r')
            iva = search.aggregate(r=Coalesce(Sum('ventImpuesto'), 0)).get('r')
            total = search.aggregate(r=Coalesce(Sum('ventTotal'), 0)).get('r')

            subtotal1=format(subtotal, '.2f')
            iva=format(iva, '.2f')
            total=format(total, '.2f')

            # print(request.POST['param'])
            template = get_template('reports/venta.html')
            # context = {'sale': CabCompra.objects.get(pk=self.kwargs['pk']),
            context = {'sale': CabCompra.objects.get(pk=1),
                       'comp': {'name': 'AlgoriSoft S.A', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador','tipo':descr},
                       'icon':'{}{}'.format(settings.MEDIA_URL, 'logo2.jpeg'),
                       'report':data,
                       'totales':{'subtotal':subtotal1,'iva':iva,'total':total}
                       # se utiliza con collectstatic
                       # 'icon':'{}{}'.format(settings.STATIC_URL, 'img/logo2.jpeg')

                       }
            html = template.render(context)
            # print('pdf no imprime')
            response = HttpResponse(content_type='application/pdf')
            # print('pdf no imprime nada')
            # para descargar el pdf
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback

            )
            # print('este no corrio')
            # if error then show some funy view
            # if pisa_status.err:
                # return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        except:
            print('pdf no imprime nada de nada')
            pass
        return HttpResponseRedirect(reverse_lazy('venta:venta_mostrar'))