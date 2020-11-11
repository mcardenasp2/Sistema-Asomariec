from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView

from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

import Sistema_Asomariec.settings as setting
from compra.models import CabCompra, DetCompra
from insumo.models import Insumo
from producto.models import Producto
from venta.models import Venta, DetVenta


class LoginFormView(LoginView):
    template_name = 'login/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context


class LogoutView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class DashboardView(TemplateView):
    template_name = 'inicio/dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_graph_sales_year_month()
                    # 'data': self.get_graph_sales_year_month(request.POST['anio'])
                }

            elif action=='get_graph_sales_products_year_month':
                data={
                    'name': 'Porcentaje',
                    # 'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_graph_sales_products_year_month()
                }
            elif action=='prueba':
                data={
                    'name':'Marco',
                    'apellido':'Cardenas'
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except:
            pass
        return JsonResponse(data, safe=False)


    def get_graph_sales_year_month(self):
        data=[]
        try:
            year = datetime.now().year
            # year=request
            for m in range(1,13):
                # total=CabCompra.objects.filter(ccoFecCom__year=year, ccoFecCom__month=m).aggregate(r=Coalesce(Sum('ccoSubtotal'), 0)).get('r')
                # data.append(float(total))
                total=Venta.objects.filter(venFechaInici__year=year, venFechaInici__month=m).aggregate(r=Coalesce(Sum('ventTotal'), 0)).get('r')
                data.append(float(total))
        except:
            pass
           # data=[1,2,3,4,5,6,7,8,9,10,11,12]
        return data

    def get_graph_sales_products_year_month(self):
        data=[]
        year = datetime.now().year
        month = datetime.now().month
        # month = 10
        try:
            # for p in Insumo.objects.all():
            #     total = DetCompra.objects.filter(cabCompra__ccoFecCom__year=year, cabCompra__ccoFecCom__month=month,cabCompra_id=p.id).aggregate(
            #         r=Coalesce(Sum('dcoSubtotal'), 0)).get('r')
            #     if total > 0:
            #         data.append({
            #             'name': p.insDescripcion,
            #             'y': float(total)
            #         })
            for p in Producto.objects.all():
                total = DetVenta.objects.filter(venta__venFechaInici__year=year, venta__venFechaInici__month=month,producto_id=p.id).aggregate(
                    r=Coalesce(Sum('detSubtotal'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.prodDescripcion,
                        'y': float(total)
                    })

        except:
            pass
        return data

    def valores(self):
        data={}
        venta=Venta.objects.all().aggregate(
                    r=Coalesce(Sum('ventTotal'), 0)).get('r')
        compra=CabCompra.objects.all().aggregate(
                    r=Coalesce(Sum('ccoTotal'), 0)).get('r')

        insumos=Insumo.objects.filter(insEstado=1).aggregate(
                    r=Coalesce(Count('insEstado'), 0)).get('r')
        producto=Producto.objects.filter(prodEstado=1).aggregate(
                    r=Coalesce(Count('prodEstado'), 0)).get('r')

        data['venta']=float(venta)
        data['compra']=float(compra)
        data['insumos']=insumos
        data['productos']=producto
        return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        # context['valor'] = { 'venta':'250.30'}
        context['valor'] = self.valores()
        return context