from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# Create your views here.
from proveedor.forms import ProveedorForm
from proveedor.models import *


class ProveedorListarView(ListView):
    model = Proveedor
    template_name = 'proveedor/proveedor/ListarProveedor.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action = request.POST['action']
            if action =='searchdata':
                # print('hola')
                data=[]
                for i in Proveedor.objects.filter(proEstado=1):
                    data.append(i.toJSON())

            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']= str(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('proveedor:proveedor_crear')
        # context['list_url'] = reverse_lazy('erp:client_list')
        context['entity'] = 'Proveedor'
        return context

class ProveedorCrearView(CreateView):
    model = Proveedor
    form_class =ProveedorForm
    template_name = 'proveedor/proveedor/FormProveedor.html'
    success_url = reverse_lazy('proveedor:proveedor_listar')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        data=[]
        try:
            action=request.POST['action']
            if action == 'add':
                form=self.get_form()
                data=form.save()
            else:
                data['error']='No ha ingresado ninguna opcion'
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('proveedor:proveedor_listar')
        context['action'] = 'add'
        return context

class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/proveedor/FormProveedor.html'
    success_url = reverse_lazy('proveedor:proveedor_listar')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                # print('hola')
                form = self.get_form()
                # form.cliFecMod = datetime.now()
                # form.cliEstado
                # print(form)
                # form("cli")
                # form.cliEstado=True
                # form['cliEstado']=True
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('proveedor:proveedor_listar')
        context['action'] = 'edit'
        return context


class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'proveedor/proveedor/DeleteProveedor.html'
    success_url = reverse_lazy('proveedor:proveedor_listar')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data={}
        try:
            action = request.POST['action']
            if action=='eliminar':
                proveedor= self.get_object()
                proveedor.proEstado=False
                proveedor.usuaEli=request.POST['usuaEli']
                proveedor.save()
            else:
                data['error']='No ha ingresado ninguna opcion'
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'eliminar'
        context['list_url'] = reverse_lazy('proveedor:proveedor_listar')
        return context

