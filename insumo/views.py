from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Vistas genericas
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
# Modelos
from insumo.models import *
# Form
from insumo.forms import *


# Create your view here.
from user.mixins import ValidatePermissionRequiredMixin


def mostrar(request):
    return render(request, 'index.html')

# Detalle Insumo Modal este utilizo
class DetalleView(LoginRequiredMixin, ValidatePermissionRequiredMixin,TemplateView):
    template_name = 'insumo/detalle_insumo/DetalleList.html'
    permission_required = 'view_unidadmedidad'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # for i in Categoria.objects.all():
                for i in UnidadMedidad.objects.filter(medEstado=1):
                    data.append(i.toJSON())

            elif action=='add':
                print('Hola amigos')
                med= UnidadMedidad()
                med.medDescripcion=request.POST['medDescripcion']
                med.medEstado=request.POST['medEstado']
                # med.usuaReg=request.POST['usuaReg']
                med.save()
                # pass
            elif action=='edit':
                # print('Hola')
                med= UnidadMedidad.objects.get(pk=request.POST['id'])
                med.medDescripcion=request.POST['medDescripcion']
                med.medEstado=request.POST['medEstado']
                # med.usuaMod=request.POST['user1']
                med.save()

            elif action=='delete':
                med= UnidadMedidad.objects.get(pk=request.POST['id'])
                med.medEstado=0
                med.usuaEli=request.POST['user1']
                med.save()

            elif action == 'searchdatacat':
                data = []
                for i in Categoria.objects.filter(catEstado=1):
                    data.append(i.toJSON())

            elif action == 'addcat':
                cat = Categoria()
                cat.catDescripcion = request.POST['catDescripcion']
                cat.catEstado = request.POST['catEstado']
                # cat.usuaReg = request.POST['usuaReg']
                cat.save()

            elif action == 'editcat':
                cat = Categoria.objects.get(pk=request.POST['id'])
                cat.catDescripcion = request.POST['catDescripcion']
                cat.catEstado = request.POST['catEstado']
                # cat.usuaMod = request.POST['user1']
                # print(request.POST['user1'])
                cat.save()

            elif action == 'deletecat':
                cat = Categoria.objects.get(pk=request.POST['id'])
                cat.catEstado = 0
                cat.usuaEli = request.POST['user1']
                cat.save()

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']= MedidaForm()
        context['form2'] = CategoriaForm()
        context['action'] = 'add'
        return context

# Categoria Modal no utilizo
class CategoriaView(LoginRequiredMixin, ValidatePermissionRequiredMixin,TemplateView):
    # model = Categoria
    permission_required = 'view_categoria'
    # template_name = 'insumo/detalle_insumo/DetalleList.html'
    template_name = 'insumo/categoria/CategoriaList.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # for i in Categoria.objects.all():
                for i in Categoria.objects.filter(catEstado=1):
                    data.append(i.toJSON())

            elif action=='add':
                print('Hola')
                cat= Categoria()
                cat.catDescripcion=request.POST['catDescripcion']
                cat.catEstado=request.POST['catEstado']
                cat.usuaReg=request.POST['usuaReg']
                # cat.usuaMod=request.POST['usuaMod']
                # cat.usuaEli=request.POST['usuaEli']
                # cat.catFecReg=request.POST['catFecReg']
                # cat.catFecMod=request.POST['catFecMod']
                # print(cat)
                cat.save()
                # pass
            elif action=='edit':
                # print('Hola')
                cat= Categoria.objects.get(pk=request.POST['id'])
                cat.catDescripcion=request.POST['catDescripcion']
                cat.catEstado=request.POST['catEstado']
                cat.usuaMod=request.POST['user1']
                print(request.POST['user1'])
                # cat.usuaMod=request.POST['usuaMod']
                # cat.usuaEli=request.POST['usuaEli']
                # cat.catFecReg=request.POST['catFecReg']
                # cat.catFecMod=request.POST['catFecMod']
                # print(cat)
                cat.save()
                # pass
            elif action=='delete':
                # print('Hola')
                cat= Categoria.objects.get(pk=request.POST['id'])
                # cat.catDescripcion=request.POST['catDescripcion']
                cat.catEstado=0
                cat.usuaEli=request.POST['user1']
                # print(request.POST['user1'])
                # cat.usuaMod=request.POST['usuaMod']
                # cat.usuaEli=request.POST['usuaEli']
                # cat.catFecReg=request.POST['catFecReg']
                # cat.catFecMod=request.POST['catFecMod']
                # print(cat)
                cat.save()
                # pass
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('insumo:categoria_mostrar')
        context['form']= CategoriaForm()
        context['action'] = 'add'
        # context['create_url'] = reverse_lazy('insumo:categoria_create')
        return context

# Modal Medida no utilizo
class MedidaView(TemplateView):
    template_name = 'insumo/medida/MedidaList.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # for i in Categoria.objects.all():
                for i in UnidadMedidad.objects.filter(medEstado=1):
                    data.append(i.toJSON())

            elif action=='add':
                # print('Hola')
                med= UnidadMedidad()
                med.medDescripcion=request.POST['medDescripcion']
                med.medEstado=request.POST['medEstado']
                med.usuaReg=request.POST['usuaReg']
                # cat.usuaMod=request.POST['usuaMod']
                # cat.usuaEli=request.POST['usuaEli']
                # cat.catFecReg=request.POST['catFecReg']
                # cat.catFecMod=request.POST['catFecMod']
                # print(cat)
                med.save()
                # pass
            elif action=='edit':
                # print('Hola')
                med= UnidadMedidad.objects.get(pk=request.POST['id'])
                med.medDescripcion=request.POST['medDescripcion']
                med.medEstado=request.POST['medEstado']
                med.usuaMod=request.POST['user1']
                # print(request.POST['user1'])
                # cat.usuaMod=request.POST['usuaMod']
                # cat.usuaEli=request.POST['usuaEli']
                # cat.catFecReg=request.POST['catFecReg']
                # cat.catFecMod=request.POST['catFecMod']
                # print(cat)
                med.save()
                # pass
            elif action=='delete':
                # print('Hola')
                med= UnidadMedidad.objects.get(pk=request.POST['id'])
                # cat.catDescripcion=request.POST['catDescripcion']
                med.medEstado=0
                med.usuaEli=request.POST['user1']
                # print(request.POST['user1'])
                # cat.usuaMod=request.POST['usuaMod']
                # cat.usuaEli=request.POST['usuaEli']
                # cat.catFecReg=request.POST['catFecReg']
                # cat.catFecMod=request.POST['catFecMod']
                # print(cat)
                med.save()
                # pass
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['list_url'] = reverse_lazy('insumo:categoria_mostrar')
        context['form']= MedidaForm()
        context['action'] = 'add'
        # context['create_url'] = reverse_lazy('insumo:categoria_create')
        return context

# Insumo

class InsumoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Insumo
    template_name = 'insumo/insumo/ListarInsumo.html'
    permission_required = 'view_insumo,delete_insumo'

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
                for i in Insumo.objects.filter(insEstado=True):
                    data.append(i.toJSON())

                # print(data)
            elif action == 'eliminar':
                insumo= Insumo.objects.get(pk=request.POST['id'])
                insumo.insEstado=False
                # usuario.usuaEli=request.POST['usuaEli']
                insumo.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('insumo:insumo_create')
        context['list_url'] = reverse_lazy('insumo:insumo_mostrar')
        context['entity'] = 'Clientes'
        return context

class InsumoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'insumo/insumo/FormInsumo.html'
    success_url = reverse_lazy('insumo:insumo_mostrar')
    permission_required = 'add_insumo'

    # def get_form(self, form_class=None):
    #     instance=self.get_object()
    #     print(instance)
    #     form=InsumoForm(instance=instance)
    #     form.fields['insPrecio'].queryset=0.00
    #     return form


    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # print(request.POST)
            # print(request.FILES)
            action = request.POST['action']
            if action == 'add':
                # print('hola')
                form = self.get_form()
                # form.insImagen
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('insumo:insumo_mostrar')
        context['title'] = 'Creación de un Insumo'
        context['action'] = 'add'
        return context

    # success_url = redirect()

class InsumoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'insumo/insumo/FormInsumo.html'
    success_url = reverse_lazy('insumo:insumo_mostrar')
    permission_required = 'change_insumo'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # print(request.FILES['insImagen'])

            # a=request.FILES['insImagen']

            # print(a)
            # print('Prueba')
            # print(request.FILES['insImagen'])
            print(request.POST)
            if action == 'edit':
                # print('hola')
                form = self.get_form()
                # print(form.insImagen['name'])
                # print(form)
                # print('Hola')
                # form.cliFecMod = datetime.now()
                # form.cliEstado
                # print(form)
                # form("cli")
                # form.cliEstado=True
                # print(form.insImagen)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('insumo:insumo_mostrar')
        context['title'] = 'Edición de un Insumo'
        context['action'] = 'edit'
        return context

class InsumoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model = Insumo
    # form_class = ClienteForm
    template_name = 'insumo/insumo/DeleteInsumo.html'
    success_url = reverse_lazy('insumo:insumo_mostrar')
    permission_required = 'delete_insumo'

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
                usuario.insEstado=False
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
        context['list_url'] = reverse_lazy('insumo:insumo_mostrar')
        return context

# no utilizo

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'insumo/categoria/CategoriaList.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # data['err'] = 'hah'
            # action = request.POST['action']
            action = request.POST['action']

            if action == 'searchdata':
                data = []
                for i in Categoria.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('insumo:categoria_mostrar')
        context['action'] = 'searchdata'
        context['create_url']=reverse_lazy('insumo:categoria_create')
        return context


class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'insumo/categoria/FormCategoria.html'
    success_url = reverse_lazy('insumo:categoria_mostrar')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                # print('hola')
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('insumo:categoria_mostrar')
        context['action'] = 'add'
        return context

    # success_url = redirect()


class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'insumo/categoria/FormCategoria.html'
    success_url = reverse_lazy('insumo:categoria_mostrar')

    # esto sirve para editar
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
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('insumo:categoria_mostrar')
        context['action'] = 'edit'
        return context


class CategoriaDelete(DeleteView):
    model = Categoria
    template_name = 'insumo/CategoriaBorrar.html'
    success_url =reverse_lazy('insumo:categoria_mostrar')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('insumo:categoria_mostrar')
        return context

