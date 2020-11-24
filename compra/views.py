import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder

from django.db import transaction
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Vistas genericas
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView, View

from django.shortcuts import render

from compra.forms import CabCompraForm
from compra.models import *

# modelo insumos
from insumo.models import Insumo

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


# from django.contrib.staticfiles import finders


# Create your views here.
from user.mixins import ValidatePermissionRequiredMixin


class CabComprListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = CabCompra
    template_name = 'compra/ListarCompra.html'
    permission_required = 'view_cabcompra'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                # print('com aqui')
                data = []
                for i in CabCompra.objects.filter(ccoEstado=True):
                    data.append(i.toJSON())

            elif action == 'search_details_ins':
                data = []
                for i in DetCompra.objects.filter(cabCompra_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('compra:compra_crear')
        context['list_url'] = reverse_lazy('compra:compra_listar')
        # context['entity'] = 'V'
        return context


class CabCompraCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = CabCompra
    form_class = CabCompraForm
    template_name = 'compra/FormCompra.html'
    success_url = reverse_lazy('insumo:insumo_mostrar')
    permission_required = 'add_cabcompra'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # print(request.POST)
            # print(request.FILES)
            action = request.POST['action']
            if action == 'search_insumos':
                # print(request.POST['term'])
                data = []
                prods = Insumo.objects.filter(insDescripcion__icontains=request.POST['term'])[0:5]
                # print(prods)
                for i in prods:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.insDescripcion
                    data.append(item)

            elif action == 'add':
                # tipo roolback
                # print('hola anadiendo 1')
                with transaction.atomic():

                    # convierto a json
                    comp = json.loads(request.POST['compras'])
                    # print(comp)
                    # print(comp['vendedor'])
                    # print(comp['cedula'])
                    # print('hola anadiendo 2')
                    cabcompra = CabCompra()
                    cabcompra.proveedor_id = comp['proveedor']
                    cabcompra.ccoVendedor = comp['vendedor']
                    cabcompra.ccoCedVend = comp['cedula']
                    cabcompra.ccoFecCom = comp['fecha']
                    cabcompra.ccoSubtotal = float(comp['subtotal'])
                    cabcompra.ccoIva = float(comp['iva'])
                    cabcompra.ccoTotal = float(comp['total'])
                    cabcompra.usuaReg = int(comp['usuaid'])
                    # print('cab compra')
                    # print(cabcompra.ccoCedVend)
                    # print(cabcompra.ccoVendedor)
                    cabcompra.save()

                    for i in comp['insumos']:
                        det = DetCompra()
                        det.cabCompra_id = cabcompra.id
                        det.insumo_id = i['id']
                        det.dcoCantidad = int(i['cant'])
                        det.dcoPreCom = float(i['insPrecio'])
                        det.dcoSubtotal = float(i['subtotal'])
                        det.save()

                        insumo = Insumo.objects.get(pk=i['id'])
                        insumo.insStock += int(i['cant'])
                        insumo.save()
                    #     esto agg para pdf
                    data={'id': cabcompra.id}

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        #     para serializar
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('compra:compra_listar')
        context['title'] = 'Creacion de una Compra'
        context['action'] = 'add'
        context['det'] = []
        return context


class CabCompraUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = CabCompra
    form_class = CabCompraForm
    template_name = 'compra/FormCompra.html'
    success_url = reverse_lazy('compra:compra_listar')
    permission_required = 'change_cabcompra'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_insumos':
                data = []
                prods = Insumo.objects.filter(insDescripcion__icontains=request.POST['term'])[0:5]
                for i in prods:
                    item = i.toJSON()
                    item['text'] = i.insDescripcion
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    comp = json.loads(request.POST['compras'])
                    # print('hola anadiendo 2')
                    cabcompra = self.get_object()
                    cabcompra.proveedor_id = comp['proveedor']
                    cabcompra.ccoVendedor = comp['vendedor']
                    cabcompra.ccoCedVend = comp['cedula']
                    cabcompra.ccoFecCom = comp['fecha']
                    cabcompra.ccoSubtotal = float(comp['subtotal'])
                    cabcompra.ccoIva = float(comp['iva'])
                    cabcompra.ccoTotal = float(comp['total'])
                    cabcompra.usuaMod = int(comp['usuaid'])
                    cabcompra.save()
                    # cabcompra.detcompra_set.all().delete()

                    for i in DetCompra.objects.filter(cabCompra_id=self.get_object().id):
                        # det = DetCompra()
                        insumo = Insumo.objects.get(pk=i.insumo_id)
                        insumo.insStock -= i.dcoCantidad
                        insumo.save()

                        # det.save()
                    cabcompra.detcompra_set.all().delete()
                    # cabcompra.detcompra_set

                    for i in comp['insumos']:
                        det = DetCompra()
                        det.cabCompra_id = cabcompra.id
                        det.insumo_id = i['id']
                        det.dcoCantidad = int(i['cant'])
                        det.dcoPreCom = float(i['insPrecio'])
                        det.dcoSubtotal = float(i['subtotal'])
                        det.save()

                        insumo = Insumo.objects.get(pk=i['id'])
                        insumo.insStock += int(i['cant'])
                        insumo.save()

                        #     esto agg para pdf
                    data = {'id': cabcompra.id}

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_insumos(self):
        data = []
        try:
            for i in DetCompra.objects.filter(cabCompra_id=self.get_object().id):
                item = i.insumo.toJSON()
                item['cant'] = i.dcoCantidad
                data.append(item)

            print('detalle');
            print(data);
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Compra'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_insumos(), cls=DjangoJSONEncoder)
        return context


class CabCompraDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = CabCompra
    # form_class = CabCompraForm
    template_name = 'compra/DeleteCompra.html'
    success_url = reverse_lazy('compra:compra_listar')
    permission_required = 'delete_detcompra'
    url_redirect = success_url

    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'delete':
                with transaction.atomic():
                    # comp = json.loads(request.POST['compras'])
                    # print('hola anadiendo 2')
                    cabcompra = self.get_object()
                    cabcompra.ccoEstado = False
                    cabcompra.save()
                    # cabcompra.detcompra_set.all().delete()

                    for i in DetCompra.objects.filter(cabCompra_id=self.get_object().id):
                        # det = DetCompra()
                        insumo = Insumo.objects.get(pk=i.insumo_id)
                        insumo.insStock -= i.dcoCantidad
                        insumo.save()

                        # det.save()
                    # cabcompra.detcompra_set.all().delete()
                    # cabcompra.detcompra_set



            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        # context['det'] = json.dumps(self.get_details_insumos(), cls=DjangoJSONEncoder)
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
            print('pdf no impr')
            template = get_template('compra/compra.html')
            context = {'sale': CabCompra.objects.get(pk=self.kwargs['pk']),
                       'comp': {'name': 'AlgoriSoft S.A', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                       'icon':'{}{}'.format(settings.MEDIA_URL, 'logo2.jpeg')
                       # se utiliza con collectstatic
                       # 'icon':'{}{}'.format(settings.STATIC_URL, 'img/logo2.jpeg')

                       }
            html = template.render(context)
            print('pdf no imprime')
            response = HttpResponse(content_type='application/pdf')
            print('pdf no imprime nada')
            # para descargar el pdf
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback

            )
            print('este no corrio')
            # if error then show some funy view
            # if pisa_status.err:
                # return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        except:
            print('pdf no imprime nada de nada')
            pass
        return HttpResponseRedirect(reverse_lazy('compra:compra_listar'))
