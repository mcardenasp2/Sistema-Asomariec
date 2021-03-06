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


# Create your views here.

class ClienteListarView(LoginRequiredMixin,ListView):
    model = Cliente
    template_name = 'cliente/ListarCliente.html'

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


class ClienteCrearView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/FormCliente.html'
    success_url = reverse_lazy('cliente:cliente_listar')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                # print('hola')
                form = self.get_form()
                form.cliFecMod=""
                form.cliFecEli = ""
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
        return context


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/FormCliente.html'
    success_url = reverse_lazy('cliente:cliente_listar')

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
        context['list_url'] = reverse_lazy('cliente:cliente_listar')
        context['action'] = 'edit'
        return context



class ClienteDeleteView(DeleteView):
    model = Cliente
    # form_class = ClienteForm
    template_name = 'cliente/DeleteCliente.html'
    success_url = reverse_lazy('cliente:cliente_listar')

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

