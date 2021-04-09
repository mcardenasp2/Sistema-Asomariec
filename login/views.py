import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your view here.
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
from datetime import timedelta

import Sistema_Asomariec.settings as setting
from compra.models import CabCompra, DetCompra
from insumo.models import Insumo
from login.forms import ResetPasswordForm, ChangePasswordForm
from producto.models import Producto
from venta.models import Venta, DetVenta


from Sistema_Asomariec.wsgi import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string

from Sistema_Asomariec import settings
from user.models import User


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


class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'inicio/dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sesion de grupos para poner el primer perfil de usuario
    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

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
            elif action=='get_ultimas_ventas':
                data=[]
                venta=Venta.objects.filter(ventEstado=True, venTipo=2)[0:4]
                for i in venta:
                    data.append([

                        i.cliente.cliNombre+' '+i.cliente.cliApellido,
                        i.venFechaFin.strftime('%Y-%m-%d'),
                        format(i.ventSubtotal, '.2f'),
                        format(i.ventImpuesto, '.2f'),
                        format(i.ventTotal, '.2f'),
                    ])
            elif action=='prueba':
                data={
                    'name':'Marco',
                    'apellido':'Cardenas'
                }
            elif action=='prueba2':
                start_date = datetime.now()
                end_date = start_date + timedelta(days=30)
                contador=Venta.objects.filter(venFechaFin__range=[start_date, end_date],ventEstado=1,venTipo=1, venEstVenta=1).order_by('venFechaFin').count()
                data={
                    'contador':contador
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
                total=Venta.objects.filter(venFechaInici__year=year, venFechaInici__month=m,ventEstado=1, venEstVenta=2).aggregate(r=Coalesce(Sum('ventTotal'), 0)).get('r')
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
            # for p in Producto.objects.all():
            for p in Producto.objects.filter(prodTipo=2):
            # for p in Producto.objects.filter(prodEstado=1):
                total = DetVenta.objects.filter(venta__venFechaInici__year=year, venta__venFechaInici__month=month,venta__ventEstado=1, venta__venEstVenta=2,producto_id=p.id).aggregate(
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
        venta=Venta.objects.filter(ventEstado=1,venEstVenta=2).aggregate(
                    r=Coalesce(Sum('ventTotal'), 0)).get('r')
        compra=CabCompra.objects.filter(ccoEstado=1).aggregate(
                    r=Coalesce(Sum('ccoTotal'), 0)).get('r')

        insumos=Insumo.objects.filter(insEstado=1).aggregate(
                    r=Coalesce(Count('insEstado'), 0)).get('r')
        producto=Producto.objects.filter(prodEstado=1,prodTipo=2).aggregate(
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

class Notificaciones(TemplateView):
    template_name = 'base/notificaciones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = Venta.objects.all()
        start_date= datetime.now()
        end_date=start_date + timedelta(days=30)
        context['form'] = Venta.objects.filter(venFechaFin__range=[start_date, end_date],ventEstado=1,venTipo=1, venEstVenta=1).order_by('venFechaFin')
        # context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        # context['valor'] = { 'venta':'250.30'}
        # context['valor'] = self.valores()
        return context


class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = 'login/resetpwd.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def send_email_reset_pwd(self, user):
        data = {}
        try:
            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()


            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            print('Hola');

            email_to = user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Reseteo de contraseña'


            content = render_to_string('login/send_email.html', {
                'user': user,
                'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                # 'link_resetpwd': '',
                # 'link_home': '/'
                'link_home': 'http://{}/login/'.format(URL)
            })
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ResetPasswordForm(request.POST)  # self.get_form()
            if form.is_valid():
                pass
                user = form.get_user()
                data = self.send_email_reset_pwd(user)
                # print('hola')
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de Contraseña'
        return context


class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = 'login/changepwd.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        print(token)
        if User.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/login/')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de Contraseña'
        context['login_url'] = settings.LOGIN_URL
        return context