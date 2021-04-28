from django.shortcuts import render
from seguridad.models import ModuloGrupo
from django.forms import model_to_dict

from django.contrib.auth.mixins import LoginRequiredMixin
from user.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from seguridad.forms import ModuloForm, GrupoModuloForm, GrupoForm
from seguridad.models import *
# Create your views here.
from django.core.serializers.json import DjangoJSONEncoder
import json

def sidebar(request):
    data = {}
    try:

        # data = {
        #     'titulo': 'Gestion de Horarios',
        #     'saludo': 'Bienvenidos Al Sistema De Gestion de Horarios',
        #     'grupos':ModuloGrupo.objects.filter(grupos=request.session['group'].id).order_by('prioridad')
        #
        # }
        data['grupos'] = ModuloGrupo.objects.filter(grupos=request.session['group'].id).order_by('prioridad')
        # data['grupos'] = ModuloGrupo.objects.filter(grupos=request.session['group'].id,
        #                                             grupos__in=request.user.groups.all()).order_by('prioridad')
        # print('Estamos')
    except:
        pass
    # addUserData(request,data)
    return render(request, 'base/sidebar.html', data)


def addUserData(request, data):
    # data['hoy'] = now
    # data['usuario'] = request.user
    # data['logo'] = LOGO_SISTEMA
    # data['sistema'] = NOMBRE_SISTEMA
    # data['institucion'] = NOMBRE_INSTITUCION
    # data['autor'] = NOMBRE_AUTOR
    # data['grupos'] = ModuloGrupo.objects.filter(grupos__in=request.user.groups.all()).order_by('prioridad')
    # print(request.session['group'].id)
    data['grupos'] = ModuloGrupo.objects.filter(grupos=request.session['group'].id,
                                                grupos__in=request.user.groups.all()).order_by('prioridad')
    print(data['grupos'])
    data['grupo'] = request.user.groups.all()[0]



class ModuloListarView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Modulo
    template_name = 'seguridad/ListarModulo.html'
    # permission_required = 'view_cliente, delete_cliente'

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
                # for i in Modulo.objects.all():
                for i in Modulo.objects.filter(activo=True):
                # for i in Empresa.objects.filter(cliEstado=True):
                    data.append(i.toJSON())

            elif action == 'eliminar':
                modulo = Modulo.objects.get(pk=request.POST['id'])
                modulo.activo = False
                modulo.save()

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('seguridad:crear_modulo')
        context['list_url'] = reverse_lazy('seguridad:mostrar_modulo')
        # context['entity'] = 'Clientes'
        return context

class ModuloCrearView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Modulo
    form_class = ModuloForm
    template_name = 'seguridad/FormModulo.html'
    success_url = reverse_lazy('seguridad:mostrar_modulo')
    # permission_required = 'add_cliente'

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
        context['list_url'] = reverse_lazy('seguridad:mostrar_modulo')
        context['action'] = 'add'
        context['title'] = 'Creación de un Módulo'
        return context



class ModuloUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Modulo
    form_class = ModuloForm
    template_name = 'seguridad/FormModulo.html'
    success_url = reverse_lazy('seguridad:mostrar_modulo')
    # permission_required = 'change_cliente'

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
        context['list_url'] = reverse_lazy('seguridad:mostrar_modulo')
        context['title'] = 'Edicion de un Módulo'
        context['action'] = 'edit'
        return context



class GrupoModuloListarView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = ModuloGrupo
    template_name = 'seguridad/grupomodulo/ListarGrupoModulo.html'
    # permission_required = 'view_cliente, delete_cliente'

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
                for i in ModuloGrupo.objects.all():
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
        context['create_url'] = reverse_lazy('seguridad:crear_grupo_modulo')
        context['list_url'] = reverse_lazy('seguridad:mostrar_grupo_modulo')
        # context['entity'] = 'Clientes'
        return context




class GrupoModuloCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = ModuloGrupo
    form_class = GrupoModuloForm
    template_name = 'seguridad/grupomodulo/FormGrupoModulo.html'
    success_url = reverse_lazy('seguridad:mostrar_grupo_modulo')
    # permission_required = 'add_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Grupo de Modulo'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class GrupoModuloUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = ModuloGrupo
    form_class = GrupoModuloForm
    template_name = 'seguridad/grupomodulo/FormGrupoModulo.html'
    success_url = reverse_lazy('seguridad:mostrar_grupo_modulo')
    # permission_required = 'change_user'
    url_redirect = success_url

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
            #     esto es mio para eleiminar la sesion


            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Grupo de Módulo'
        # context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context



class GrupoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Group
    form_class = GrupoForm
    template_name = 'seguridad/grupo/FormGrupo.html'
    success_url = reverse_lazy('seguridad:mostrar_grupo')
    # permission_required = 'add_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Rol y Permisos'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class GrupoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Group
    form_class = GrupoForm
    template_name = 'seguridad/grupo/FormGrupo.html'
    success_url = reverse_lazy('seguridad:mostrar_grupo')
    # permission_required = 'change_user'
    url_redirect = success_url

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
            #     esto es mio para eleiminar la sesion


            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Rol y Permisos'
        # context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context





class GrupoListarView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Group
    template_name = 'seguridad/grupo/ListarGrupo.html'
    # permission_required = 'view_cliente, delete_cliente'

    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def toJSON(Group):
    #     item=model_to_dict(Group)
    #         # item['grupos'] = [{'id': g.id, 'nombre': g.name} for g in self.grupos.all()]
    #     item['permissions'] = [{'id': g.id, 'nombre': g.name} for g in self.permissions.all()]
    #     return  item

    # def toJSON(self):
    #     item=model_to_dict(self)
    #     # item['grupos'] = [{'id': g.id, 'nombre': g.name} for g in self.grupos.all()]
    #     item['permissions'] = [{'id': g.id, 'name': g.name} for g in self.permissions.all()]
    #     return  item

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                # print('Nose')
                # print(self.toJSON())
                data = []
                # data=json.dumps(self.get_details_produtos(), cls=DjangoJSONEncoder)

                #         item=model_to_dict(self)
                #         # item['grupos'] = [{'id': g.id, 'nombre': g.name} for g in self.grupos.all()]
                #         item['permissions'] = [{'id': g.id, 'nombre': g.name} for g in self.permissions.all()]
                #         return  item
                # data=Group.objects.all()
                # for i in ModuloGrupo.objects.all():
                for i in Group.objects.all():
                    item = model_to_dict(i)
                    # print(item)
                    item['permissions'] = [{'id': g.id, 'name': g.name} for g in i.permissions.all()]
                # for i in Empresa.objects.filter(cliEstado=True):
                    data.append(item)
                # print(data)


            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('seguridad:crear_grupo')
        context['list_url'] = reverse_lazy('seguridad:mostrar_grupo')
        # context['entity'] = 'Clientes'
        return context