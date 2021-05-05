from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from cliente.models import *
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cliente.forms import *


# Create your view here.
from user.mixins import ValidatePermissionRequiredMixin


class ClienteListarView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Cliente
    template_name = 'cliente/ListarCliente.html'
    permission_required = [('view_cliente','delete_cliente')]
    # permission_required = 'view_cliente'

    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # for i in Cliente.objects.all():
                for i in Cliente.objects.filter(cliEstado=True):
                    data.append(i.toJSON())
            elif action == 'eliminar':
                cliente = Cliente.objects.get(pk=request.POST['id'])
                cliente.cliEstado = 0
                cliente.save()

                # usuario = self.get_object()
                # usuario.cliEstado = False
                # usuario.usuaEli = request.POST['usuaEli']
                # usuario.save()


            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('cliente:cliente_crear')
        # context['list_url'] = reverse_lazy('erp:client_list')
        context['entity'] = 'Clientes'
        return context


class ClienteCrearView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/FormCliente.html'
    success_url = reverse_lazy('cliente:cliente_listar')
    permission_required = 'add_cliente'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                # print('hola')
                form = self.get_form()
                # form.cliFecMod=""
                # form.cliFecEli = ""
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('cliente:cliente_listar')
        context['action'] = 'add'
        context['title'] = 'Creación de un Cliente'
        return context


class ClienteUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/FormCliente.html'
    success_url = reverse_lazy('cliente:cliente_listar')
    permission_required = 'change_cliente'

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
                # print(form.user_creation)

                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('cliente:cliente_listar')
        context['title'] = 'Edicion de un Cliente'
        context['action'] = 'edit'
        return context



class ClienteDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model = Cliente
    # form_class = ClienteForm
    template_name = 'cliente/DeleteCliente.html'
    success_url = reverse_lazy('cliente:cliente_listar')
    permission_required = 'delete_cliente'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data = {}

        # print("hola")
        try:
            action = request.POST['action']
            if action == 'eliminar':
                # print('hola')
                usuario= self.get_object()
                usuario.cliEstado=False
                # print('Hola')
                # fec=usuario.cliFecMod
                # print(fec)
                usuario.usuaEli=request.POST['usuaEli']
                # usuario.cliFecMod = fec
                # usuario.cliFecEli = datetime.now()
                # usuario.cliFecEli=datetime.now()
                usuario.save()
                # form = self.get_form()
                # data = form.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'eliminar'
        context['list_url'] = reverse_lazy('cliente:cliente_listar')
        return context

    # def get_queryset(self):
    #
    #     if self.request.user.is_superuser:
    #         return User.objects.all()
    #     else:
    #         return User.objects.filter(is_superuser=False)

# class ClienteDeleteView(UpdateView):
#     model = Cliente
#     form_class = ClienteForm
#     template_name = 'cliente/DeleteCliente.html'
#     success_url = reverse_lazy('cliente:cliente_listar')
#
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'eliminar':
#                 # print('hola')
#                 form = self.get_form()
#                 data = form.save()
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['action'] = 'eliminar'
#         context['list_url'] = reverse_lazy('insumo:categoria_mostrar')
#         return context
#
#     # def get_queryset(self):
#     #
#     #     if self.request.user.is_superuser:
#     #         return User.objects.all()
#     #     else:
#     #         return User.objects.filter(is_superuser=False)

# def ClienteDelete(request, personas_id):
#     instancia= Cliente.objects.get(id=personas_id)
#
#     instancia.cliEstado=0
#
#     data = {}
#     try:
#         instancia.save()
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data)

