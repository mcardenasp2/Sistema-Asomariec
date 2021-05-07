from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
# Create your view here.
from proveedor.forms import ProveedorForm
from proveedor.models import *
from user.mixins import ValidatePermissionRequiredMixin


class ProveedorListarView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Proveedor
    template_name = 'proveedor/proveedor/ListarProveedor.html'
    # permission_required = 'view_proveedor','delete_proveedor'
    permission_required = 'view_proveedor'
    # , 'delete_proveedor'

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
            # elif action=='eliminar':
            #     proveedor= Proveedor.objects.get(pk=request.POST['id'])
            #     proveedor.proEstado=False
            #     # proveedor.usuaEli=request.POST['usuaEli']
            #     proveedor.save()
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

class ProveedorCrearView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Proveedor
    form_class =ProveedorForm
    template_name = 'proveedor/proveedor/FormProveedor.html'
    success_url = reverse_lazy('proveedor:proveedor_listar')
    permission_required = 'add_proveedor'

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

class ProveedorUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/proveedor/FormProveedor.html'
    success_url = reverse_lazy('proveedor:proveedor_listar')
    permission_required = 'change_proveedor'

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


class ProveedorDelete(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    # model = Cliente
    # template_name = 'cliente/ListarCliente.html'
    # success_url = reverse_lazy('cliente:cliente_listar')
    permission_required = 'delete_proveedor'
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
                proveedor = Proveedor.objects.get(pk=request.POST['id'])
                proveedor.proEstado = False
                # proveedor.usuaEli=request.POST['usuaEli']
                proveedor.save()
                data['success']="Correcto"
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        # return HttpResponseRedirect(reverse_lazy('cliente:cliente_listar'))
        return JsonResponse(data)


class ProveedorDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model = Proveedor
    template_name = 'proveedor/proveedor/DeleteProveedor.html'
    success_url = reverse_lazy('proveedor:proveedor_listar')
    permission_required = 'delete_proveedor'

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

