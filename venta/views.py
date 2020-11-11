import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from insumo.models import Insumo
from producto.models import Producto, DetProducto
from venta.models import *

from django.views.generic import CreateView,ListView, UpdateView, DeleteView

from venta.forms import CabVentaForm

class VentaListView(ListView):
    template_name = 'venta/normal/ListarVenta.html'
    model = Venta

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
                for i in Venta.objects.filter(ventEstado=True,venTipo=2):
                    data.append(i.toJSON())

            elif action == 'search_details_ins':
                data = []
                for i in DetVenta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
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


class VentaCreateView(CreateView):
    model = Venta
    form_class = CabVentaForm
    template_name = 'venta/normal/FormVenta.html'

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
                prods = Producto.objects.filter(prodDescripcion__icontains=request.POST['term'],prodCantidad__gte=1)[0:5]
                # print(prods)
                for i in prods:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.prodDescripcion
                    data.append(item)

            elif action=='add':
                with transaction.atomic():
                    vent=json.loads(request.POST['ventas'])
                    # print(prod);
                    cabventa= Venta()
                    cabventa.cliente_id= vent['cliente']
                    cabventa.venFechaInici=vent['fecha']
                    # cabventa.venFechaFin=vent['cliente']
                    cabventa.ventObservacion='Ninguna'
                    cabventa.venTipo=2
                    cabventa.ventTotal=float(vent['tgsto'])+float(vent['subproductos'])
                    cabventa.ventEstado=1
                    cabventa.save()

                    for i in vent['productos']:
                        det=DetVenta()
                        det.venta_id=cabventa.id
                        det.producto_id=i['id']
                        det.detCant=i['cant']
                        det.detPrecio=i['prodPrecio']
                        det.detSubtotal=i['subtotal']
                        det.save()

                        producto=Producto.objects.get(pk=i['id'])
                        producto.prodCantidad-=int(i['cant'])
                        producto.save()

                    if vent['gastoad']:
                        for i in vent['gastoad']:
                            gast= GastAdc()
                            gast.venta_id=cabventa.id
                            gast.gastdescripcion=i['gastDescripcion']
                            gast.gastprecio=i['gastPrecio']
                            gast.save()



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
        context['det']=[]
        context['gasta']=[]
        return context



class VentaUpdateView(UpdateView):
    template_name = 'venta/normal/FormVenta.html'
    model = Venta
    form_class = CabVentaForm
    success_url = reverse_lazy('venta:venta_mostrar')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

            elif action == 'edit':
                with transaction.atomic():
                    vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    cabventa = self.get_object()
                    cabventa.cliente_id = vent['cliente']
                    cabventa.venFechaInici = vent['fecha']
                    # cabventa.venFechaFin=vent['cliente']
                    cabventa.ventObservacion = 'Ninguna'
                    cabventa.venTipo = 2
                    cabventa.ventTotal = float(vent['tgsto']) + float(vent['subproductos'])
                    cabventa.ventEstado = 1
                    cabventa.save()

                    for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                        producto = Producto.objects.get(pk=i.producto_id)
                        producto.prodCantidad+=i.detCant
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
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_produtos(self):
        data=[]
        try:
            for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                item=i.producto.toJSON()
                item['cant']=i.detCant
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
        context['det'] = json.dumps(self.get_details_produtos(), cls=DjangoJSONEncoder)
        context['gasta'] = json.dumps(self.get_details_gastos(), cls=DjangoJSONEncoder)
        return context




# contrato
class VentaContratoListView(ListView):
    template_name = 'venta/contrato/ListarVenta.html'
    model = Venta

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
                for i in Venta.objects.filter(ventEstado=True,venTipo=1):
                    data.append(i.toJSON())

            elif action == 'search_details_ins':
                data = []
                for i in DetVenta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
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



class VentaContratoCreateView(CreateView):
    template_name = 'venta/contrato/FormVenta.html'
    form_class = CabVentaForm
    model = Venta

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
                    cabventa.venFechaInici = vent['fecha']
                    cabventa.venFechaFin=vent['fechafin']
                    cabventa.ventObservacion = 'Ninguna'
                    cabventa.venTipo = 1
                    cabventa.ventTotal = float(vent['tgsto']) + float(vent['subproductos'])
                    cabventa.ventEstado = 1
                    cabventa.save()



                    for i in vent['productos']:
                        prd = Producto()
                        prd.prodDescripcion=i['prodDescripcion']
                        prd.prodTipo=1
                        prd.prodCantidad=i['cant']
                        prd.prodPrecio=i['prodPrecio']
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

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        #     para serializar
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['list_url'] = reverse_lazy('compra:compra_listar')
        context['action'] = 'add'
        # context['create_url'] = 'add'
        context['det']=[]
        context['gasta']=[]
        return context

# tomar en cuenta el guardado del producto
class VentaContratoUpdateView(UpdateView):
    template_name = 'venta/contrato/FormVenta.html'
    model = Venta
    form_class = CabVentaForm
    success_url = reverse_lazy('venta:ventac_mostrar')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

            elif action == 'edit':

                print('que paso')
                with transaction.atomic():
                    vent = json.loads(request.POST['ventas'])
                    # print(prod);
                    cabventa = self.get_object()
                    cabventa.cliente_id = vent['cliente']
                    cabventa.venFechaInici = vent['fecha']
                    cabventa.venFechaFin = vent['fechafin']
                    # cabventa.venFechaFin=vent['cliente']
                    cabventa.ventObservacion = 'Ninguna'
                    cabventa.venTipo = 1
                    cabventa.ventTotal = float(vent['tgsto']) + float(vent['subproductos'])
                    cabventa.ventEstado = 1
                    cabventa.save()

                    # a={}
                    # contiene el id del producto
                    c=[]


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
                        if i['id']==0:
                            print('aggrego')
                            prd = Producto()
                            prd.prodDescripcion = i['prodDescripcion']
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
        context['det'] = json.dumps(self.get_details_produtos(), cls=DjangoJSONEncoder)
        context['gasta'] = json.dumps(self.get_details_gastos(), cls=DjangoJSONEncoder)
        return context



class VentaDeleteView(DeleteView):
    template_name = 'venta/DeleteVenta.html'
    model = Venta
    # form_class = CabVentaForm
    success_url = reverse_lazy('venta:venta_mostrar')

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


class VentaDeleteContratoView(DeleteView):
    template_name = 'venta/DeleteVenta.html'
    model = Venta
    # form_class = CabVentaForm
    success_url = reverse_lazy('venta:ventac_mostrar')

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
                    cabventa.save()

                    c = []
                    for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                        c.append(i.producto_id)

                    # for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                    #     producto = Producto.objects.get(pk=i.producto_id)
                    #     producto.prodCantidad += i.detCant
                    #     producto.save()

                    cabventa.detventa_set.all().delete()

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
                        producto = Producto.objects.get(pk=i)
                        producto.detproducto_set.all().delete()
                        producto.delete();


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