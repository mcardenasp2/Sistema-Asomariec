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
from producto.models import Producto, DetProducto, GastosAdicionales
from insumo.models import Insumo
from producto.forms import ProductoForm
from user.mixins import ValidatePermissionRequiredMixin


class ProductoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Producto
    template_name = 'producto/ListarProducto.html'
    permission_required = 'view_producto'

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
                for i in Producto.objects.filter(prodEstado=True, prodEstprod=True, prodTipo=2):
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
        # context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('producto:producto_create')
        context['list_url'] = reverse_lazy('producto:producto_mostrar')
        # context['entity'] = 'V'
        return context

class ProductoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/FormProducto.html'
    permission_required = 'add_producto'

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

                    cabprod= Producto()
                    cabprod.prodDescripcion=prod['producto']
                    if request.FILES.get('imagen1'):
                        cabprod.prodImagen = request.FILES['imagen1']

                    if request.FILES.get('imagen2'):
                        cabprod.prodImagen2 = request.FILES['imagen2']

                    # cabprod.prodImagen=request.FILES['imagen1']
                    # cabprod.prodImagen2=request.FILES['imagen2']
                    cabprod.prodCantidad=prod['cantidad']
                    cabprod.prodPrecio=float(prod['precio'])
                    cabprod.prodTotal=float(prod['total'])
                    cabprod.prodIva=float(prod['iva'])
                    # cabprod.prodCaracteristica=prod['']
                    cabprod.prodCaracteristica=prod['detalle']
                    cabprod.prodEstprod=1
                    cabprod.prodTipo=2
                    # cabprod.prodEstado=prod['']
                    cabprod.usuaReg=1
                    cabprod.save()
                    # print(cabprod.prodTotal)

                    for i in prod['insumos']:
                        det = DetProducto()
                        det.producto_id=cabprod.id
                        det.insumo_id=i['id']
                        det.detCantidad=i['cant']
                        det.detprecio=i['insPrecio']
                        det.detSubtotal=i['subtotal']
                        det.save()

                        insumo = Insumo.objects.get(pk=i['id'])
                        insumo.insStock -= int(i['cant'])
                        insumo.save()

                        # print(prod['insumos'])
                        # print(prod['gastosad'])

                    # if prod['gastosad']:
                    #     # print('gastos adici')
                    #     for i in prod['gastosad']:
                    #         gast = GastosAdicionales()
                    #         gast.producto_id = cabprod.id
                    #         # print(i)
                    #         # print('gastos adici x1')
                    #         gast.gastdescripcion = i['gastDescripcion']
                    #         # print('gastos adici x2')
                    #         gast.gastprecio = float(i['gastPrecio'])
                    #         gast.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        #     para serializar
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('producto:producto_mostrar')
        context['action'] = 'add'
        context['det']=[]
        # context['gasta']=[]
        return context

class ProductoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    template_name = 'producto/FormProducto.html'
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('producto:producto_mostrar')
    permission_required = 'change_producto'

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
                # gte mayor lte menor
                prods = Insumo.objects.filter(insDescripcion__icontains=request.POST['term'],insStock__gte=1, insEstado=1)[0:5]
                # print(prods)
                for i in prods:
                    item = i.toJSON()
                    # jquery ui
                    # item['value'] = i.insDescripcion
                    # select 2
                    item['text'] = i.insDescripcion
                    data.append(item)


            elif action=='edit':
                with transaction.atomic():
                    prod= json.loads(request.POST['compras'])


                    cabprod= self.get_object()
                    cabprod.prodDescripcion=prod['producto']
                    # print('sumare')

                    # print(request.FILES)
                    if request.FILES.get('imagen1'):
                        cabprod.prodImagen = request.FILES['imagen1']

                    if request.FILES.get('imagen2'):
                        cabprod.prodImagen2 = request.FILES['imagen2']
                    cabprod.prodCantidad=prod['cantidad']
                    cabprod.prodPrecio=float(prod['precio'])
                    cabprod.prodTotal=float(prod['total'])
                    cabprod.prodIva=float(prod['iva'])
                    # cabprod.prodCaracteristica=prod['']
                    cabprod.prodCaracteristica=prod['detalle']
                    cabprod.prodEstprod=1
                    # cabprod.prodTipo=2
                    # cabprod.prodEstado=prod['']
                    cabprod.usuaReg=1
                    cabprod.save()
                    # print(cabprod.prodTotal)
                    for i in DetProducto.objects.filter(producto_id=self.get_object().id):
                        insumo=Insumo.objects.get(pk=i.insumo_id)
                        insumo.insStock+=i.detCantidad
                        insumo.save()

                    cabprod.detproducto_set.all().delete()


                    for i in prod['insumos']:
                        det = DetProducto()
                        det.producto_id=cabprod.id
                        det.insumo_id=i['id']
                        det.detCantidad=i['cant']
                        det.detprecio=i['insPrecio']
                        # det.detSubtotal=i['subtotal']
                        # borrar
                        det.detSubtotal=0.00
                        det.save()

                        insumo = Insumo.objects.get(pk=i['id'])
                        insumo.insStock -= int(i['cant'])
                        insumo.save()

                        # print(prod['insumos'])
                        # print(prod['gastosad'])

                    cabprod.gastosadicionales_set.all().delete()

                    # if prod['gastosad']:
                    #     # print('gastos adici')
                    #     for i in prod['gastosad']:
                    #         gast = GastosAdicionales()
                    #         gast.producto_id = cabprod.id
                    #         # print(i)
                    #         # print('gastos adici x1')
                    #         gast.gastdescripcion = i['gastDescripcion']
                    #         # print('gastos adici x2')
                    #         gast.gastprecio = float(i['gastPrecio'])
                    #         gast.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        #     para serializar
        return JsonResponse(data, safe=False)


    def get_details_insumos(self):
        data = []
        try:
            for i in DetProducto.objects.filter(producto_id=self.get_object().id):
                item = i.insumo.toJSON()
                item['cant'] = i.detCantidad
                data.append(item)

            # print('detalle');
            # print(data);
        except:
            pass
        return data

    # def get_details_gastos(self):
    #     data = []
    #     try:
    #         for i in GastosAdicionales.objects.filter(producto_id=self.get_object().id):
    #             item = {}
    #             item['gastDescripcion'] = i.gastdescripcion
    #             item['gastPrecio'] = float(i.gastprecio)
    #             data.append(item)
    #
    #     except:
    #         pass
    #     return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Edición de una Venta'
        # context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_insumos(), cls=DjangoJSONEncoder)
        # context['gasta'] = json.dumps(self.get_details_gastos(), cls=DjangoJSONEncoder)
        return context

class ProductoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    template_name = 'producto/DeleteProducto.html'
    model = Producto
    # form_class = ProductoForm
    success_url = reverse_lazy('producto:producto_mostrar')
    permission_required = 'delete_producto'

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
                    cabprod.prodEstado=False
                    cabprod.save()
                    # print(cabprod.prodTotal)
                    for i in DetProducto.objects.filter(producto_id=self.get_object().id):
                        insumo=Insumo.objects.get(pk=i.insumo_id)
                        insumo.insStock+=i.detCantidad
                        insumo.save()

                    # cabprod.detproducto_set.all().delete()

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



class ProductListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Producto
    template_name = 'producto/product/ListProduct.html'
    permission_required = 'add_producto, delete_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                print('entro')
                data = []
                for i in Producto.objects.filter(prodEstado=True, prodEstprod=True, prodTipo=2):
                    data.append(i.toJSON())
            elif action == 'eliminar':

                prod = Producto.objects.get(pk=request.POST['id'])
                prod.prodEstado = False
                # prod.usuaEli = request.POST['usuaEli']
                prod.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('producto:product_create')
        context['list_url'] = reverse_lazy('producto:product_mostrar')
        return context

class ProductCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/product/FormProduct.html'
    # permission_required = 'add_producto'

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
                form= self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
               data['error'] = str(e)
        #     para serializar
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('producto:product_mostrar')
        context['action'] = 'add'
        return context

class ProductUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    template_name = 'producto/product/FormProduct.html'
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('producto:product_mostrar')
    # permission_required = 'change_producto'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('producto:product_mostrar')
        # context['title'] = 'Edicion de un Insumo'
        context['action'] = 'edit'
        return context

class ProductDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    template_name = 'producto/product/DeleteProduct.html'
    model = Producto
    success_url = reverse_lazy('producto:product_mostrar')
    # permission_required = 'delete_producto'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'eliminar':
                prod = self.get_object()
                prod.prodEstado = False
                # prod.usuaEli = request.POST['usuaEli']
                prod.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'eliminar'
        context['list_url'] = reverse_lazy('producto:product_mostrar')
        return context