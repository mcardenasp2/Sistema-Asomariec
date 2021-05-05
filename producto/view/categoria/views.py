from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView

from producto.models import Categoria
from producto.forms import CategoriaForm
from user.mixins import ValidatePermissionRequiredMixin


class DetalleCategoriaView(LoginRequiredMixin, ValidatePermissionRequiredMixin,TemplateView):
    template_name = 'producto/categoria/FormCategoria.html'
    permission_required = 'view_categoria','delete_categoria','change_categoria','add_categoria'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action = request.POST['action']
            if action== 'add':
                # print('Proband')
                categoria= Categoria()
                categoria.catDescripcion=request.POST['catDescripcion']
                categoria.save()
            elif action=='searchdata':
                data=[]
                for i in Categoria.objects.filter(catEstado=1):
                # for i in Categoria.objects.all():
                    # print(i.toJSON)
                    data.append(i.toJSON())
                # print('ggg')
                # print(data)
            elif action=='edit':
                categoria= Categoria.objects.get(pk=request.POST['id'])
                categoria.catDescripcion=request.POST['catDescripcion']
                categoria.save()
            elif action=='delete':
                categoria=Categoria.objects.get(pk=request.POST['id'])
                categoria.catEstado=0
                categoria.save()
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoriaForm()
        context['action'] = 'add'
        return context

# class CategoriaListView(ListView):
#     model = Categoria
#     template_name = 'producto/categoria/ShowCategoria.html'
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'searchdata':
#                 data = []
#                 for i in Categoria.objects.all():
#                     data.append(i.toJSON())
#             else:
#                 data['error'] = 'Ha ocurrido un error'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data, safe=False)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['create_url'] = reverse_lazy('producto:categoria_mostrar')
#         context['list_url'] = reverse_lazy('producto:categoria_mostrar')
#         return context
#
# class CategoriaCreateView(CreateView):
#     model = Categoria
#     template_name = 'producto/categoria/FormCategoria.html'
#     success_url = reverse_lazy('producto:categoria_mostrar')
#     # url_redirect=success_url
#
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'add':
#                 form = self.get_form()
#                 data = form.save()
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['title'] = 'Creación un Cliente'
#         # context['entity'] = 'Clientes'
#         context['list_url'] = self.success_url
#         context['action'] = 'add'
#         return context
