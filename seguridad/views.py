from django.shortcuts import render
from seguridad.models import ModuloGrupo


# Create your views here.


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
