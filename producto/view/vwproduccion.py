import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder

from django.shortcuts import render
from django.db import transaction
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
# Create your view here.
from producto.models import Producto, DetProducto, GastosAdicionales,Produccion
from insumo.models import Insumo
from producto.forms import ProduccionForm
from user.mixins import ValidatePermissionRequiredMixin


class ProduccionListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model=Produccion
    template_name = 'producto/produccion/ListarProduccion.html'
    permission_required = 'view_produccion'

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
                # for i in Produccion.objects.filter(prodcEstado=True, prodEstprod=True, prodTipo=2):
                # for i in Produccion.objects.filter(prodcEstado=True, prodcTipo=2):
                for i in Produccion.objects.filter(prodcEstado=True, prodcTipo=1):
                    data.append(i.toJSON())
                # data.sort('prodcFecElab')

            elif action == 'search_details_ins':
                data = []
                for i in DetProducto.objects.filter(produccion__id=request.POST['id']):
                    data.append(i.toJSON())

            # elif action == 'search_details_ins':
            #     data = []
            #     for i in DetCompra.objects.filter(cabCompra_id=request.POST['id']):
            #         data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('producto:produccion_create')
        context['list_url'] = reverse_lazy('producto:produccion_mostrar')
        return context


class ProducionCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Produccion
    form_class = ProduccionForm
    success_url = reverse_lazy('producto:produccion_mostrar')
    template_name = 'producto/produccion/FormProduccion.html'
    permission_required = 'add_produccion'
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
            if action == 'search_insumos':
                # print(request.POST['term'])

                ids=json.loads(request.POST['ids'])
                # print(type(ids))
                data = []
                prods = Insumo.objects.filter(insDescripcion__icontains=request.POST['term'],insStock__gte=1, insEstado=1)
                # print(prods)
                for i in prods.exclude(id__in=ids)[0:5]:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.insDescripcion
                    data.append(item)

            elif action=='add':
                with transaction.atomic():
                    prod= json.loads(request.POST['compras'])

                    prcc=Produccion()
                    prcc.producto_id=prod['producto']
                    prcc.prodcCantidad=prod['cantidad']
                    prcc.prodcFecElab=prod['fecha']
                    prcc.prodcTotal=float(prod['totalproduc'])
                    prcc.save()
                    # print(prcc.prodcCantidad)
                    # print(prcc.prodcFecElab)
                    # print(prcc.prodcTotal)
                    # print(prcc.prodcCantidad)


                    # cabprod= Producto()

                    # print('Hola')
                    # print(cabprod)
                    # cabprod.prodDescripcion=prod['producto']
            #         if request.FILES.get('imagen1'):
            #             cabprod.prodImagen = request.FILES['imagen1']
            #
            #         if request.FILES.get('imagen2'):
            #             cabprod.prodImagen2 = request.FILES['imagen2']
            #
            #         # cabprod.prodImagen=request.FILES['imagen1']
            #         # cabprod.prodImagen2=request.FILES['imagen2']
            #         cabprod.prodCantidad+=int(prcc.prodcCantidad)
                    # cabprod.prodPrecio=float(prod['precio'])
                    # cabprod.prodTotal=float(prod['total'])
            #         cabprod.prodIva=float(prod['iva'])
            #         # cabprod.prodCaracteristica=prod['']
            #         cabprod.prodCaracteristica=prod['detalle']
            #         cabprod.prodEstprod=1
            #         cabprod.prodTipo=2
            #         # cabprod.prodEstado=prod['']
            #         cabprod.usuaReg=1
            #         cabprod.save()
            #         # print(cabprod.prodTotal)
            #
                    for i in prod['insumos']:
                        det = DetProducto()
                        det.produccion_id=prcc.id
                        det.insumo_id=i['id']
                        det.detCantidad=i['cant']
                        # det.detprecio=i['insPrecio']
                        det.detprecio=i['instotalprecio']
                        det.detSubtotal=i['subtotal']
                        det.save()

                        insumo = Insumo.objects.get(pk=i['id'])
                        insumo.insStock -= int(i['cant'])
                        insumo.save()

                    cabprod = Producto.objects.get(pk=prcc.producto_id)
                    cabprod.prodCantidad += int(prcc.prodcCantidad)
                    cabprod.save()
            #
            #             # print(prod['insumos'])
            #             # print(prod['gastosad'])
            #


            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        #     para serializar
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('producto:produccion_mostrar')
        context['action'] = 'add'
        context['det']=[]
        # context['gasta']=[]
        return context


class ProduccionDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    template_name = 'producto/produccion/DeleteProduccion.html'
    model = Produccion
    # form_class = ProductoForm
    success_url = reverse_lazy('producto:produccion_mostrar')
    # permission_required = 'delete_producto'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data = {}
        try:
            # print(request.POST)
            # print(request.FILES)
            action = request.POST['action']

            if action=='delete':
                with transaction.atomic():
                    # prod= json.loads(request.POST['compras'])

                    cabprod= self.get_object()
                    cabprod.prodcEstado=False
                    cabprod.save()
                    # print(cabprod.prodTotal)
                    for i in DetProducto.objects.filter(produccion_id=self.get_object().id):
                        insumo=Insumo.objects.get(pk=i.insumo_id)
                        insumo.insStock+=i.detCantidad
                        insumo.save()

                    # cabprod.detproducto_set.all().delete()
                    # print(cabprod.prodcCantidad)

                    prod = Producto.objects.get(pk=cabprod.producto_id)
                    prod.prodCantidad -= int(cabprod.prodcCantidad)
                    # print(prod.prodCantidad)
                    prod.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        #     para serializar
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Edición de una Venta'
        # context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        # context['det'] = json.dumps(self.get_details_insumos(), cls=DjangoJSONEncoder)
        # context['gasta'] = json.dumps(self.get_details_gastos(), cls=DjangoJSONEncoder)
        return context

