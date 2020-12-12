"""Sistema_Asomariec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.shortcuts import render,HttpResponse
from django.urls import path, include

def mostrar(request):
    # return render(request, 'base/body.html')
    return render(request, 'test.html')
def mostrar2(request):
    # return render(request, 'base/body.html')
    return render(request, 'base/notificaciones.html')

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hola/', mostrar),
    # path('hola/prueba/', mostrar2),
    path('prueba/', mostrar2),
    path('insumo/', include('insumo.urls')),
    path('cliente/', include('cliente.urls')),
    path('proveedor/', include('proveedor.urls')),
    path('compra/', include('compra.urls')),
    path('producto/', include('producto.urls')),
    path('venta/', include('venta.urls')),
    path('login/', include('login.urls')),
    path('reports/', include('reports.urls')),
    path('user/', include('user.urls')),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)