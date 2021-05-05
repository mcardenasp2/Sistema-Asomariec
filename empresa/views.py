from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from user.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from empresa.models import *
from empresa.forms import EmpresaForm

class EmpresaListarView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Empresa
    template_name = 'empresa/ListarEmpresa.html'
    permission_required = 'view_empresa'

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
                for i in Empresa.objects.all():
                # for i in Empresa.objects.filter(cliEstado=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Listado de Clientes'
        # context['create_url'] = reverse_lazy('cliente:cliente_crear')
        # context['list_url'] = reverse_lazy('erp:client_list')
        # context['entity'] = 'Clientes'
        return context



class EmpresaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/FormEmpresa.html'
    success_url = reverse_lazy('empresa:empresa_listar')
    permission_required = 'change_empresa'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
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
        context['list_url'] = reverse_lazy('empresa:empresa_listar')
        context['title'] = 'Edicion de Empresa'
        context['action'] = 'edit'
        return context