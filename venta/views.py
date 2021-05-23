import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render

# Create your view here.
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from cliente.forms import ClienteForm, ContratoForm
from insumo.models import Insumo
from producto.models import Producto, DetProducto, Produccion
from user.mixins import ValidatePermissionRequiredMixin
from venta.models import *

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View

from venta.forms import CabVentaForm

from empresa.models import Empresa


from cliente.models import Contrato
from producto.forms import ProductoForm

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


class VentaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    template_name = 'venta/normal/ListarVenta.html'
    model = Venta
    # permission_required = 'view_venta','delete_venta'
    permission_required = 'view_venta'

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
                for i in Venta.objects.filter(ventEstado=True, venTipo=2):
                    data.append(i.toJSON())

            elif action == 'search_details_ins':
                data = []
                for i in DetVenta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == "search_gastos":
                data = []
                for i in GastAdc.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            # elif action == 'eliminar':
            #     with transaction.atomic():
            #         # vent = json.loads(request.POST['ventas'])
            #         # print(prod);
            #             # print('Eliminar')
            #         # cabventa = self.get_object()
            #         cabventa = Venta.objects.get(pk=request.POST['id'])
            #         cabventa.ventEstado = False
            #         cabventa.venEstVenta = 1
            #         cabventa.save()
            #
            #         for i in DetVenta.objects.filter(venta_id=cabventa.id):
            #             producto = Producto.objects.get(pk=i.producto_id)
            #             producto.prodCantidad += i.detCant
            #             producto.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('venta:venta_create')
        context['list_url'] = reverse_lazy('venta:venta_mostrar')
        # context['entity'] = 'V'
        return context


class VentaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Venta
    form_class = CabVentaForm
    # template_name = 'venta/normal/FormVenta.html'
    success_url = reverse_lazy('venta:venta_mostrar')
    template_name = 'venta/normal/FormVentaNuevo.html'
    permission_required = 'add_venta'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # print(request.POST)
            # print(request.FILES)
            action = request.POST['action']
            if action == 'search_productos':
                # print(request.POST['term'])
                data = []
                # me retorna un string y lo cambio a lista
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                print(type(ids_exclude))
                print(ids_exclude)
                prueba = [1, 2]
                prods = Producto.objects.filter(prodDescripcion__icontains=term, prodCantidad__gt=0,
                                                prodTipo=2, prodEstado=1)

                print(prods)
                for i in prods.exclude(pk__in=ids_exclude)[0:5]:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.prodDescripcion
                    data.append(item)
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                # este es el for que se utiliza en django
                # , cliEstado=1
                clients = Cliente.objects.filter(
                    Q(cliNombre__icontains=term) | Q(cliApellido__icontains=term) | Q(cliRuc__contains=term),
                    cliEstado=1)[0:10]
                # print(prods)
                for i in clients:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                # print(request.POST)
                with transaction.atomic():
                    frmCLient = ClienteForm(request.POST)
                    data = frmCLient.save()

            elif action == 'add':
                with transaction.atomic():
                    vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    cabventa = Venta()
                    cabventa.cliente_id = vent['cliente']
                    cabventa.venFechaFin = vent['fecha']
                    cabventa.venFechaInici = vent['fecha']
                    cabventa.ventSubtotal = float(vent['subproductos']) + float(vent['tgsto'])
                    cabventa.ventImpuesto = float(vent['impuestos'])
                    cabventa.ventDescuento = float(vent['descuento'])
                    cabventa.ventTotalDescuento = float(vent['totaldescuento'])
                    cabventa.ventObservacion = 'Ninguna'
                    cabventa.venTipo = 2
                    cabventa.ventTotal = float(vent['tgsto']) + float(vent['subproductos']) + float(vent['impuestos'])-float(vent['totaldescuento'])
                    cabventa.ventEstado = 1
                    cabventa.venEstVenta = 2
                    cabventa.save()

                    for i in vent['productos']:
                        det = DetVenta()
                        det.venta_id = cabventa.id
                        det.producto_id = i['id']
                        det.detCant = i['cant']
                        det.detPrecio = i['prodPrecio']
                        det.detSubtotal = i['subtotal']
                        det.save()

                        producto = Producto.objects.get(pk=i['id'])
                        producto.prodCantidad -= int(i['cant'])
                        producto.save()

                    if vent['gastoad']:
                        for i in vent['gastoad']:
                            gast = GastAdc()
                            gast.venta_id = cabventa.id
                            gast.gastdescripcion = i['gastDescripcion']
                            gast.gastprecio = i['gastPrecio']
                            gast.save()

                    data = {'id': cabventa.id}



            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        #     para serializar
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('venta:venta_mostrar')
        context['action'] = 'add'
        context['frmClient'] = ClienteForm()
        context['det'] = []
        context['gasta'] = []
        return context


class VentaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    template_name = 'venta/normal/FormVenta.html'
    model = Venta
    form_class = CabVentaForm
    success_url = reverse_lazy('venta:venta_mostrar')
    permission_required = 'change_venta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = CabVentaForm(instance=instance)
        # queryset necesita un listado
        form.fields['cliente'].queryset = Cliente.objects.filter(id=instance.cliente.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_productos':
                # print(request.POST['term'])
                data = []
                prods = Producto.objects.filter(prodDescripcion__icontains=request.POST['term'], prodCantidad__gt=0,
                                                prodTipo=2, prodEstado=1)[
                        0:5]
                # print(prods)
                for i in prods:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.prodDescripcion
                    data.append(item)
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                # este es el for que se utiliza en django
                # , cliEstado=1
                clients = Cliente.objects.filter(
                    Q(cliNombre__icontains=term) | Q(cliApellido__icontains=term) | Q(cliRuc__contains=term),
                    cliEstado=1)[0:10]
                # print(prods)
                for i in clients:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.get_full_name()
                    data.append(item)

            elif action == 'create_client':
                # print(request.POST)
                with transaction.atomic():
                    frmCLient = ClienteForm(request.POST)
                    data = frmCLient.save()
            elif action == 'edit':
                with transaction.atomic():
                    vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    cabventa = self.get_object()
                    cabventa.cliente_id = vent['cliente']
                    cabventa.venFechaFin = vent['fecha']
                    # cabventa.venFechaFin=vent['cliente']
                    cabventa.ventSubtotal = float(vent['subproductos']) + float(vent['tgsto'])
                    cabventa.ventImpuesto = float(vent['impuestos'])
                    cabventa.ventObservacion = 'Ninguna'
                    cabventa.venTipo = 2
                    cabventa.ventTotal = float(vent['tgsto']) + float(vent['subproductos']) + float(vent['impuestos'])
                    cabventa.ventEstado = 1
                    # cabventa.venEstVenta = 2
                    # cabventa.ventEstado =2
                    cabventa.save()

                    for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                        producto = Producto.objects.get(pk=i.producto_id)
                        producto.prodCantidad += i.detCant
                        producto.save()

                    cabventa.detventa_set.all().delete()

                    for i in vent['productos']:
                        det = DetVenta()
                        det.venta_id = cabventa.id
                        det.producto_id = i['id']
                        det.detCant = i['cant']
                        det.detPrecio = i['prodPrecio']
                        det.detSubtotal = i['subtotal']
                        det.save()

                        producto = Producto.objects.get(pk=i['id'])
                        producto.prodCantidad -= int(i['cant'])
                        producto.save()

                    cabventa.gastadc_set.all().delete()

                    if vent['gastoad']:
                        for i in vent['gastoad']:
                            gast = GastAdc()
                            gast.venta_id = cabventa.id
                            gast.gastdescripcion = i['gastDescripcion']
                            gast.gastprecio = i['gastPrecio']
                            gast.save()
                    data = {'id': cabventa.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_produtos(self):
        data = []
        try:
            for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                item = i.producto.toJSON()
                item['cant'] = i.detCant
                data.append(item)
        except:
            pass
        return data

    def get_details_gastos(self):
        data = []
        try:
            for i in GastAdc.objects.filter(venta_id=self.get_object().id):
                item = {}
                item['gastDescripcion'] = i.gastdescripcion
                item['gastPrecio'] = float(i.gastprecio)
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Edición de una Venta'
        # context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['frmClient'] = ClienteForm()
        context['det'] = json.dumps(self.get_details_produtos(), cls=DjangoJSONEncoder)
        context['gasta'] = json.dumps(self.get_details_gastos(), cls=DjangoJSONEncoder)
        return context


class VentaDelete(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    # model = Cliente
    # template_name = 'cliente/ListarCliente.html'
    # success_url = reverse_lazy('cliente:cliente_listar')
    permission_required = 'delete_venta'
    # url_redirect = success_url


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # print(self.request)
        return super().dispatch(request, *args, **kwargs)

    # @permission_required('delete_cliente')
    def post(self, request, *args, **kwargs):
        data = {}

        try:
            action = request.POST['action']
            # print('eliminar')
            if action == 'eliminar':
                with transaction.atomic():
                    # vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    # print('Eliminar')
                    # cabventa = self.get_object()
                    cabventa = Venta.objects.get(pk=request.POST['id'])
                    cabventa.ventEstado = False
                    cabventa.venEstVenta = 1
                    cabventa.save()

                    for i in DetVenta.objects.filter(venta_id=cabventa.id):
                        producto = Producto.objects.get(pk=i.producto_id)
                        producto.prodCantidad += i.detCant
                        producto.save()
                    data['success']="Correcto"
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        # return HttpResponseRedirect(reverse_lazy('cliente:cliente_listar'))
        return JsonResponse(data)

class VentaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    template_name = 'venta/DeleteVenta.html'
    model = Venta
    # form_class = CabVentaForm
    success_url = reverse_lazy('venta:venta_mostrar')
    permission_required = 'delete_venta'

    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'delete':
                with transaction.atomic():
                    # vent = json.loads(request.POST['ventas'])
                    # print(prod);
                        # print('Eliminar')
                    cabventa = self.get_object()
                    cabventa.ventEstado = False
                    cabventa.venEstVenta = 1
                    cabventa.save()

                    for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                        producto = Producto.objects.get(pk=i.producto_id)
                        producto.prodCantidad += i.detCant
                        producto.save()

                    # cabventa.detventa_set.all().delete()

                    # cabventa.gastadc_set.all().delete()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Edición de una Venta'
        # context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        # context['det'] = json.dumps(self.get_details_produtos(), cls=DjangoJSONEncoder)
        # context['gasta'] = json.dumps(self.get_details_gastos(), cls=DjangoJSONEncoder)
        return context


class SaleInvoicePdfView(View):

    def link_callback(self, uri, rel):
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
            template = get_template('venta/normal/invoice2.html')
            # item={}
            det = []

            data = Venta.objects.get(pk=self.kwargs['pk']).toJSON()
            # det= DetVenta.objects.get(venta=self.kwargs['pk'])
            for i in DetVenta.objects.filter(venta=self.kwargs['pk']):
                item = i.producto.toJSON()
                item['imp'] = format(i.producto.prodIva * i.detPrecio * i.detCant, '.2f')
                item['cant'] = i.detCant
                item['subt'] = i.detSubtotal
                item['deta'] = i.producto.toJSON()
                det.append(item)

            gast = []
            for i in GastAdc.objects.filter(venta=self.kwargs['pk']):
                gast.append(i)

            idventa=Venta.objects.get(pk=self.kwargs['pk'])

            empresa = Empresa.objects.get(pk=1).toJSON()

            creaadordeventa=User.objects.get(pk=idventa.user_creation_id).toJSON()
            # print(creaadordeventa['full'])

            context = {'sale': Venta.objects.get(pk=self.kwargs['pk']),
                       'vendedor':creaadordeventa['full_name'],
                       # context = {'sale': data,
                       # 'comp': {'name': 'AlgoriSoft S.A', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                       'comp': empresa,
                       'icon': '{}{}'.format(settings.MEDIA_URL, 'logo2.jpeg'),
                       'nfact': data['nfact'],
                       'fec': data['venFechaInici'],
                       'det': det,
                       'gastad': gast
                       # se utiliza con collectstatic
                       # 'icon':'{}{}'.format(settings.STATIC_URL, 'img/logo2.jpeg')

                       }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # para descargar el pdf
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback

            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('venta:venta_mostrar'))


# contrato
class VentaContratoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    template_name = 'venta/contrato/ListarVenta.html'
    model = Venta
    permission_required = 'view_venta'

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
                for i in Venta.objects.filter(ventEstado=True, venTipo=1):
                    data.append(i.toJSON())

            elif action == 'search_details_ins':
                data = []
                for i in DetVenta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            # elif action == 'eliminar':
            #     with transaction.atomic():
            #         # vent = json.loads(request.POST['ventas'])
            #         # print(prod);
            #         # cabventa = self.get_object()
            #         cabventa = Venta.objects.get(pk=request.POST['id'])
            #         cabventa.ventEstado = False
            #         cabventa.venEstVenta = 1
            #         cabventa.save()
            #
            #         for i in DetVenta.objects.filter(venta_id=cabventa.id):
            #             producto = Producto.objects.get(pk=i.producto_id)
            #             producto.prodCantidad += i.detCant
            #             if producto.prodEstprod==1:
            #                 producto.prodTipo=2
            #             producto.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('venta:ventacont_create')
        context['list_url'] = reverse_lazy('venta:ventac_mostrar')
        # context['entity'] = 'V'
        return context


class VentaContratoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    template_name = 'venta/contrato/FormVentaNuevo.html'
    form_class = CabVentaForm
    success_url = reverse_lazy('venta:ventac_mostrar')
    model = Venta
    permission_required = 'add_venta'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # print(request.POST)
            # print(request.FILES)
            action = request.POST['action']

            if action == 'add':
                with transaction.atomic():
                    vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    cabventa = Venta()
                    cabventa.cliente_id = vent['cliente']
                    cabventa.venEstVenta = vent['ventestado']
                    cabventa.venFechaInici = vent['fecha']
                    cabventa.venFechaFin = vent['fechafin']
                    cabventa.ventSubtotal = float(vent['subproductos']) + float(vent['tgsto'])
                    cabventa.ventImpuesto = float(vent['impuestos'])
                    cabventa.ventDescuento = float(vent['descuento'])
                    cabventa.ventTotalDescuento = float(vent['totaldescuento'])
                    cabventa.ventObservacion = vent['observacion']



                    cabventa.venTipo = 1
                    cabventa.ventTotal = float(vent['tgsto']) + float(vent['subproductos']) + +float(vent['impuestos'])-float(vent['totaldescuento'])
                    cabventa.ventEstado = 1
                    cabventa.save()
                    # Aggreo a la tabla contratos
                    contrato=Contrato()
                    contrato.cliente_id=vent['cliente']
                    contrato.contratoDescripcion=vent['observacion']
                    contrato.contratoFec_Inicio=vent['fecha']
                    contrato.contratoFec_Fin=vent['fechafin']
                    contrato.save()



                    for i in vent['productos']:
                        prd = Producto()
                        prd.prodDescripcion = i['prodDescripcion']
                        prd.prodIva = i['prodIva']
                        prd.prodTipo = 1
                        prd.prodEstprod=2
                        # prd.prodEstado=False
                        # prd.prodCantidad = i['cant']
                        prd.prodCantidad = 0
                        prd.prodPrecio = i['prodPrecio']

                        prd.categoria_id=i['categoria']
                        prd.save()

                        det = DetVenta()
                        det.venta_id = cabventa.id
                        # det.producto_id = i['id']
                        det.producto_id = prd.id
                        det.detCant = i['cant']
                        det.detPrecio = i['prodPrecio']
                        det.detSubtotal = i['subtotal']
                        det.save()

                        # producto = Producto.objects.get(pk=i['id'])
                        # producto.prodCantidad -= int(i['cant'])
                        # producto.save()

                    if vent['gastoad']:
                        for i in vent['gastoad']:
                            gast = GastAdc()
                            gast.venta_id = cabventa.id
                            gast.gastdescripcion = i['gastDescripcion']
                            gast.gastprecio = i['gastPrecio']
                            gast.save()

                    data = {'id': cabventa.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                # este es el for que se utiliza en django
                # , cliEstado=1
                clients = Cliente.objects.filter(
                    Q(cliNombre__icontains=term) | Q(cliApellido__icontains=term) | Q(cliRuc__contains=term),
                    cliEstado=1)[0:10]
                # print(prods)
                for i in clients:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                # print(request.POST)
                with transaction.atomic():
                    frmCLient = ClienteForm(request.POST)
                    data = frmCLient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        #     para serializar
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('venta:ventac_mostrar')
        context['action'] = 'add'
        # context['create_url'] = 'add'
        context['frmClient'] = ClienteForm()
        context['frmProducto'] =ProductoForm()
        context['det'] = []
        context['gasta'] = []
        return context


class VentaContratoDelete(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    # model = Cliente
    # template_name = 'cliente/ListarCliente.html'
    # success_url = reverse_lazy('cliente:cliente_listar')
    permission_required = 'delete_venta'
    # url_redirect = success_url


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # print(self.request)
        return super().dispatch(request, *args, **kwargs)

    # @permission_required('delete_cliente')
    def post(self, request, *args, **kwargs):
        data = {}

        try:
            action = request.POST['action']
            # print('eliminar')
            if action == 'eliminar':
                with transaction.atomic():
                    # vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    # cabventa = self.get_object()
                    cabventa = Venta.objects.get(pk=request.POST['id'])
                    cabventa.ventEstado = False
                    cabventa.venEstVenta = 1
                    cabventa.save()

                    for i in DetVenta.objects.filter(venta_id=cabventa.id):
                        producto = Producto.objects.get(pk=i.producto_id)
                        producto.prodCantidad += i.detCant
                        if producto.prodEstprod == 1:
                            producto.prodTipo = 2
                        producto.save()
                    data['success']="Correcto"
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        # return HttpResponseRedirect(reverse_lazy('cliente:cliente_listar'))
        return JsonResponse(data)


class VentaContratoDetalleView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    template_name = 'venta/contrato/DetalleVentaNuevo.html'
    model = Venta
    form_class = CabVentaForm
    success_url = reverse_lazy('venta:ventac_mostrar')
    permission_required = 'change_venta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = CabVentaForm(instance=instance)
        # queryset necesita un listado
        form.fields['cliente'].queryset = Cliente.objects.filter(id=instance.cliente.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_insumos':
                # print(request.POST['term'])

                ids = json.loads(request.POST['ids'])
                # ids = []
                # print(type(ids))
                data = []
                prods = Insumo.objects.filter(insDescripcion__icontains=request.POST['term'], insStock__gte=1,
                                              insEstado=1)
                # print(prods)
                for i in prods.exclude(id__in=ids)[0:5]:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.insDescripcion
                    data.append(item)

            elif action=='searchdata':
                data=[]
                for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                    item = i.producto.toJSON()
                    item['cant'] = i.detCant
                    data.append(item)

            elif action == 'create_produccion':
                # print(request.POST)
                with transaction.atomic():

                    prod = json.loads(request.POST['insumos'])

                    prcc = Produccion()
                    prcc.producto_id = prod['producto']
                    prcc.prodcCantidad = prod['cantidad']
                    prcc.prodcFecElab = prod['fecha']
                    prcc.prodcTotal = float(prod['totalproduc'])
                    prcc.save()
                    for i in prod['insumos']:
                        det = DetProducto()
                        det.produccion_id = prcc.id
                        det.insumo_id = i['id']
                        det.detCantidad = i['cant']
                        # det.detprecio = i['insPrecio']
                        det.detprecio = i['instotalprecio']
                        det.detSubtotal = i['subtotal']
                        det.save()

                        insumo = Insumo.objects.get(pk=i['id'])
                        insumo.insStock -= int(i['cant'])
                        insumo.save()

                    cabprod = Producto.objects.get(pk=prcc.producto_id)
                    cabprod.prodCantidad += int(prcc.prodcCantidad)
                    # cabprod.save()
                    # cabprod = Producto.objects.get(pk=prod['producto'])
                    cabprod.prodEstprod=1
                    cabprod.save()

            elif action == 'edit':

                # print('que paso')
                with transaction.atomic():
                    vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    cabventa = self.get_object()
                    # cabventa.cliente_id = vent['cliente']
                    cabventa.venEstVenta = vent['ventestado']
                    # cabventa.venFechaInici = vent['fecha']
                    # cabventa.venFechaFin = vent['fechafin']
                    # print(float(vent['tgsto']))

                    # cabventa.ventSubtotal = float(vent['subproductos']) + float(vent['tgsto'])
                    # cabventa.ventSubtotal = float(vent['subproductos'])
                    # cabventa.ventImpuesto = float(vent['impuestos'])
                    # cabventa.venFechaFin=vent['cliente']
                    # cabventa.ventObservacion = 'Ninguna'
                    cabventa.venTipo = 1
                    # cabventa.ventTotal = float(vent['tgsto']) + float(vent['subproductos']) + float(vent['impuestos'])
                    cabventa.ventEstado = 1
                    cabventa.save()
                    print(cabventa.venEstVenta)
                    if cabventa.venEstVenta=='2':
                        for i in vent['productos']:
                            prd = Producto.objects.get(pk=i['id'])
                            # print('Hola')
                            # print(prd.prodCantidad)
                            # print('Chao')
                            # print(i['cant'])
                            prd.prodCantidad -= i['cant']
                            prd.save()


                    # a={}
                    # contiene el id del producto
                    # c = []

                    # for i in DetVenta.objects.filter(venta_id=7):
                    #     print(i.producto_id)
                    #     c.append(i.producto_id)
                    #     print(c)

                    # for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                        # for i in DetVenta.objects.filter(venta_id=7):
                        #     print(i.producto_id)
                        #     a['id']=i.producto_id
                        # c.append(i.producto_id)
                        # print(c)
                        # producto = Producto.objects.get(pk=i.producto_id)
                        # producto.delete();
                        # producto.prodCantidad += i.detCant
                        # producto.save()
                    # print(c)
                    # p=[]
                    # p=c

                    # cabventa.detventa_set.all().delete()
                    # detalle del producto
                    # insu = []
                    # for p in c:
                    # for i in DetProducto.objects.filter(producto_id=p):
                    # insu.append(i.insumo_id)
                    # item=i.insumo.toJSON()
                    # item['cant']=i.detCantidad
                    # insu.append(item)

                    # insumo = Insumo.objects.get(pk=i.insumo_id)
                    # insumo.insStock += i.detCantidad
                    # insumo.save()
                    #
                    # for i in vent['productos']:
                    #     if i['id'] == 0:
                    #         print('aggrego')
                    #         prd = Producto()
                    #         prd.prodDescripcion = i['prodDescripcion']
                    #         prd.prodIva = i['prodIva']
                    #         prd.prodEstado = False
                    #         prd.prodCantidad = i['cant']
                    #         prd.prodPrecio = i['prodPrecio']
                    #         prd.save()
                    #
                    #         det = DetVenta()
                    #         det.venta_id = cabventa.id
                    #         det.producto_id = prd.id
                    #         det.detCant = i['cant']
                    #         det.detPrecio = i['prodPrecio']
                    #         det.detSubtotal = i['subtotal']
                    #         det.save()
                    #
                    #     elif i['id'] in c:
                    #         print('si estas ' + str(i['id']))
                    #
                    #         # edito el produto 16/11/2020
                    #         prd = Producto.objects.get(pk=i['id'])
                    #         prd.prodDescripcion = i['prodDescripcion']
                    #         prd.prodIva = i['prodIva']
                    #         prd.prodEstado = False
                    #         prd.prodCantidad = i['cant']
                    #         prd.prodPrecio = i['prodPrecio']
                    #         prd.save()
                    #
                    #         det = DetVenta()
                    #         det.venta_id = cabventa.id
                    #         det.producto_id = i['id']
                    #         det.detCant = i['cant']
                    #         det.detPrecio = i['prodPrecio']
                    #         det.detSubtotal = i['subtotal']
                    #         det.save()
                    #         c.remove(i['id'])

                            # print('no agrego')
                    # print(p)

                    # for i in c:
                    #     for v in vent['productos']:
                    #         if i==v['id']:
                    #             pass

                    # for v in vent['productos']:
                    #     if v['id'] in c:
                    #         print('si esta '+ str(v['id']))

                    # for i in c:
                    #     for d in DetProducto.objects.filter(producto_id=i):
                    #         insumo = Insumo.objects.get(pk=d.insumo_id)
                    #         insumo.insStock += d.detCantidad
                    #         insumo.save()
                    #     # cabprod = Producto()
                    #     # cabprod.detproducto_set.all().delete()
                    #
                    #     producto = Producto.objects.get(pk=i)
                    #     producto.detproducto_set.all().delete()
                    #
                    #     producto.delete();

                    # print('este men')
                    # for i in vent['productos']:
                    #     prd = Producto()
                    #     prd.prodDescripcion = i['prodDescripcion']
                    #     prd.prodCantidad = i['cant']
                    #     prd.prodPrecio = i['prodPrecio']
                    #
                    #     print('mmmmmmmmmmmmmmmmmmm')
                    #     prd.save()
                    #
                    #     det = DetVenta()
                    #     det.venta_id = cabventa.id
                    #     det.producto_id = prd.id
                    #     det.detCant = i['cant']
                    #     det.detPrecio = i['prodPrecio']
                    #     det.detSubtotal = i['subtotal']
                    #     det.save()

                    # producto = Producto.objects.get(pk=i['id'])
                    # producto.prodCantidad -= int(i['cant'])
                    # producto.save()

                    # cabventa.gastadc_set.all().delete()

                    # if vent['gastoad']:
                    #     for i in vent['gastoad']:
                    #         gast = GastAdc()
                    #         gast.venta_id = cabventa.id
                    #         gast.gastdescripcion = i['gastDescripcion']
                    #         gast.gastprecio = i['gastPrecio']
                    #         gast.save()
                    #
                    data = {'id': cabventa.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_produtos(self):
        data = []
        try:
            for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                item = i.producto.toJSON()
                item['cant'] = i.detCant
                data.append(item)
        except:
            pass
        return data

    def get_details_gastos(self):
        data = []
        try:
            for i in GastAdc.objects.filter(venta_id=self.get_object().id):
                item = {}
                item['gastDescripcion'] = i.gastdescripcion
                item['gastPrecio'] = float(i.gastprecio)
                data.append(item)
        except:
            pass
        return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frmClient'] = ClienteForm()
        # context['frmContrato'] = ContratoForm.
        # context['title'] = 'Edición de una Venta'
        # context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_produtos(), cls=DjangoJSONEncoder)
        # context['det'] = []
        context['gasta'] = json.dumps(self.get_details_gastos(), cls=DjangoJSONEncoder)
        return context


# tomar en cuenta el guardado del producto
class VentaContratoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    template_name = 'venta/contrato/FormVenta.html'
    model = Venta
    form_class = CabVentaForm
    success_url = reverse_lazy('venta:ventac_mostrar')
    permission_required = 'change_venta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = CabVentaForm(instance=instance)
        # queryset necesita un listado
        form.fields['cliente'].queryset = Cliente.objects.filter(id=instance.cliente.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_productos':
                # print(request.POST['term'])
                data = []
                prods = Producto.objects.filter(prodDescripcion__icontains=request.POST['term'], prodCantidad__gte=1)[
                        0:5]
                # print(prods)
                for i in prods:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.prodDescripcion
                    data.append(item)
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                # este es el for que se utiliza en django
                # , cliEstado=1
                clients = Cliente.objects.filter(
                    Q(cliNombre__icontains=term) | Q(cliApellido__icontains=term) | Q(cliRuc__contains=term),
                    cliEstado=1)[0:10]
                # print(prods)
                for i in clients:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                # print(request.POST)
                with transaction.atomic():
                    frmCLient = ClienteForm(request.POST)
                    data = frmCLient.save()
            elif action == 'edit':

                # print('que paso')
                with transaction.atomic():
                    vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    cabventa = self.get_object()
                    cabventa.cliente_id = vent['cliente']
                    cabventa.venEstVenta = vent['ventestado']
                    cabventa.venFechaInici = vent['fecha']
                    cabventa.venFechaFin = vent['fechafin']
                    # print(float(vent['tgsto']))

                    cabventa.ventSubtotal = float(vent['subproductos']) + float(vent['tgsto'])
                    # cabventa.ventSubtotal = float(vent['subproductos'])
                    cabventa.ventImpuesto = float(vent['impuestos'])
                    # cabventa.venFechaFin=vent['cliente']
                    cabventa.ventObservacion = 'Ninguna'
                    cabventa.venTipo = 1
                    cabventa.ventTotal = float(vent['tgsto']) + float(vent['subproductos']) + float(vent['impuestos'])
                    cabventa.ventEstado = 1
                    cabventa.save()

                    # a={}
                    # contiene el id del producto
                    c = []

                    # for i in DetVenta.objects.filter(venta_id=7):
                    #     print(i.producto_id)
                    #     c.append(i.producto_id)
                    #     print(c)

                    for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                        # for i in DetVenta.objects.filter(venta_id=7):
                        #     print(i.producto_id)
                        #     a['id']=i.producto_id
                        c.append(i.producto_id)
                        # print(c)
                        # producto = Producto.objects.get(pk=i.producto_id)
                        # producto.delete();
                        # producto.prodCantidad += i.detCant
                        # producto.save()
                    # print(c)
                    # p=[]
                    # p=c

                    cabventa.detventa_set.all().delete()
                    # detalle del producto
                    # insu = []
                    # for p in c:
                    # for i in DetProducto.objects.filter(producto_id=p):
                    # insu.append(i.insumo_id)
                    # item=i.insumo.toJSON()
                    # item['cant']=i.detCantidad
                    # insu.append(item)

                    # insumo = Insumo.objects.get(pk=i.insumo_id)
                    # insumo.insStock += i.detCantidad
                    # insumo.save()

                    for i in vent['productos']:
                        if i['id'] == 0:
                            print('aggrego')
                            prd = Producto()
                            prd.prodDescripcion = i['prodDescripcion']
                            prd.prodIva = i['prodIva']
                            prd.prodEstado = False
                            prd.prodCantidad = i['cant']
                            prd.prodPrecio = i['prodPrecio']
                            prd.save()

                            det = DetVenta()
                            det.venta_id = cabventa.id
                            det.producto_id = prd.id
                            det.detCant = i['cant']
                            det.detPrecio = i['prodPrecio']
                            det.detSubtotal = i['subtotal']
                            det.save()

                        elif i['id'] in c:
                            print('si estas ' + str(i['id']))

                            # edito el produto 16/11/2020
                            prd = Producto.objects.get(pk=i['id'])
                            prd.prodDescripcion = i['prodDescripcion']
                            prd.prodIva = i['prodIva']
                            prd.prodEstado = False
                            prd.prodCantidad = i['cant']
                            prd.prodPrecio = i['prodPrecio']
                            prd.save()

                            det = DetVenta()
                            det.venta_id = cabventa.id
                            det.producto_id = i['id']
                            det.detCant = i['cant']
                            det.detPrecio = i['prodPrecio']
                            det.detSubtotal = i['subtotal']
                            det.save()
                            c.remove(i['id'])

                            # print('no agrego')
                    # print(p)

                    # for i in c:
                    #     for v in vent['productos']:
                    #         if i==v['id']:
                    #             pass

                    # for v in vent['productos']:
                    #     if v['id'] in c:
                    #         print('si esta '+ str(v['id']))

                    for i in c:
                        for d in DetProducto.objects.filter(producto_id=i):
                            insumo = Insumo.objects.get(pk=d.insumo_id)
                            insumo.insStock += d.detCantidad
                            insumo.save()
                        # cabprod = Producto()
                        # cabprod.detproducto_set.all().delete()

                        producto = Producto.objects.get(pk=i)
                        producto.detproducto_set.all().delete()

                        producto.delete();

                    # print('este men')
                    # for i in vent['productos']:
                    #     prd = Producto()
                    #     prd.prodDescripcion = i['prodDescripcion']
                    #     prd.prodCantidad = i['cant']
                    #     prd.prodPrecio = i['prodPrecio']
                    #
                    #     print('mmmmmmmmmmmmmmmmmmm')
                    #     prd.save()
                    #
                    #     det = DetVenta()
                    #     det.venta_id = cabventa.id
                    #     det.producto_id = prd.id
                    #     det.detCant = i['cant']
                    #     det.detPrecio = i['prodPrecio']
                    #     det.detSubtotal = i['subtotal']
                    #     det.save()

                    # producto = Producto.objects.get(pk=i['id'])
                    # producto.prodCantidad -= int(i['cant'])
                    # producto.save()

                    cabventa.gastadc_set.all().delete()

                    if vent['gastoad']:
                        for i in vent['gastoad']:
                            gast = GastAdc()
                            gast.venta_id = cabventa.id
                            gast.gastdescripcion = i['gastDescripcion']
                            gast.gastprecio = i['gastPrecio']
                            gast.save()

                    data = {'id': cabventa.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_produtos(self):
        data = []
        try:
            for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                item = i.producto.toJSON()
                item['cant'] = i.detCant
                data.append(item)
        except:
            pass
        return data

    def get_details_gastos(self):
        data = []
        try:
            for i in GastAdc.objects.filter(venta_id=self.get_object().id):
                item = {}
                item['gastDescripcion'] = i.gastdescripcion
                item['gastPrecio'] = float(i.gastprecio)
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frmClient'] = ClienteForm()
        # context['title'] = 'Edición de una Venta'
        # context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_produtos(), cls=DjangoJSONEncoder)
        context['gasta'] = json.dumps(self.get_details_gastos(), cls=DjangoJSONEncoder)
        return context


class VentaDeleteContratoView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    template_name = 'venta/DeleteVenta.html'
    model = Venta
    # form_class = CabVentaForm
    success_url = reverse_lazy('venta:ventac_mostrar')
    permission_required = 'delete_venta'

    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'delete':
                with transaction.atomic():
                    # vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    cabventa = self.get_object()
                    cabventa.ventEstado = False
                    cabventa.venEstVenta = 1
                    cabventa.save()

                    for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                        producto = Producto.objects.get(pk=i.producto_id)
                        producto.prodCantidad += i.detCant
                        if producto.prodEstprod==1:
                            producto.prodTipo=2
                        producto.save()

                    # c = []
                    # for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                    #     c.append(i.producto_id)

                    # for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                    #     producto = Producto.objects.get(pk=i.producto_id)
                    #     producto.prodCantidad += i.detCant
                    #     producto.save()
                    # print('no')
                    # cabventa.detventa_set.all().delete()
                    # print('si')

                    # insu=[]
                    # for p in c:
                    #     for i in DetProducto.objects.filter(producto_id=p):
                            # insu.append(i.insumo_id)
                            # item = i.insumo.toJSON()
                            # item['cant'] = i.detCantidad
                            # insu.append(item)
                            #
                            # insumo = Insumo.objects.get(pk=i.insumo_id)
                            # insumo.insStock += i.detCantidad
                            # insumo.save()

                    # for i in c:
                    #     print('yi')
                    #     producto = Producto.objects.get(pk=i)
                    #     producto.detproducto_set.all().delete()
                    #     print('yo')
                    #     producto.delete();
                    #     print('yes')
                    #
                    # print('ya')
                    # cabventa.gastadc_set.all().delete()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Edición de una Venta'
        # context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        # context['det'] = json.dumps(self.get_details_produtos(), cls=DjangoJSONEncoder)
        # context['gasta'] = json.dumps(self.get_details_gastos(), cls=DjangoJSONEncoder)
        return context


class VentaDeleteContratoViewno(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    template_name = 'venta/DeleteVenta.html'
    model = Venta
    # form_class = CabVentaForm
    success_url = reverse_lazy('venta:ventac_mostrar')
    permission_required = 'delete_venta'

    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'delete':
                with transaction.atomic():
                    # vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    cabventa = self.get_object()
                    cabventa.ventEstado = False
                    cabventa.venEstVenta = 1
                    cabventa.save()

                    c = []
                    for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                        c.append(i.producto_id)

                    # for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                    #     producto = Producto.objects.get(pk=i.producto_id)
                    #     producto.prodCantidad += i.detCant
                    #     producto.save()
                    # print('no')
                    cabventa.detventa_set.all().delete()
                    # print('si')

                    # insu=[]
                    for p in c:
                        for i in DetProducto.objects.filter(producto_id=p):
                            # insu.append(i.insumo_id)
                            # item = i.insumo.toJSON()
                            # item['cant'] = i.detCantidad
                            # insu.append(item)

                            insumo = Insumo.objects.get(pk=i.insumo_id)
                            insumo.insStock += i.detCantidad
                            insumo.save()

                    for i in c:
                        print('yi')
                        producto = Producto.objects.get(pk=i)
                        producto.detproducto_set.all().delete()
                        print('yo')
                        producto.delete();
                        print('yes')

                    print('ya')
                    # cabventa.gastadc_set.all().delete()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Edición de una Venta'
        # context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        # context['det'] = json.dumps(self.get_details_produtos(), cls=DjangoJSONEncoder)
        # context['gasta'] = json.dumps(self.get_details_gastos(), cls=DjangoJSONEncoder)
        return context
