from django.urls import path

from seguridad.views import *

app_name = 'seguridad'

urlpatterns = [
    path('sidebar/', sidebar, name='sidebar'),

    # modulos
    path('modulo/mostrar', ModuloListarView.as_view(), name='mostrar_modulo'),
    path('modulo/crear', ModuloCrearView.as_view(), name='crear_modulo'),
    path('modulo/editar/<int:pk>/', ModuloUpdateView.as_view(), name='modulo_editar'),

    # grupo de modulos
    path('grupomodulo/mostrar', GrupoModuloListarView.as_view(), name='mostrar_grupo_modulo'),
    path('grupomodulo/crear', GrupoModuloCreateView.as_view(), name='crear_grupo_modulo'),
    path('grupomodulo/editar/<int:pk>/', GrupoModuloUpdateView.as_view(), name='editar_grupo_modulo'),

    # grupo roles y permisos
    path('grupo/mostrar', GrupoListarView.as_view(), name='mostrar_grupo'),
    path('grupo/crear', GrupoCreateView.as_view(), name='crear_grupo'),
    path('grupo/editar/<int:pk>/', GrupoUpdateView.as_view(), name='editar_grupo'),
    path('grupo/eliminar/', DeleteGrupo.as_view(), name='eliminar_grupo'),


    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # path('notificaciones/', Notificaciones.as_view(), name='notificaciones'),
    # path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    # path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password')
    # # path('logout/', LogoutRedirectView.as_view(), name='logout')
]
