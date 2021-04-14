from django.urls import path

from seguridad.views import *

urlpatterns = [
    path('sidebar/', sidebar, name='sidebar'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # path('notificaciones/', Notificaciones.as_view(), name='notificaciones'),
    # path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    # path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password')
    # # path('logout/', LogoutRedirectView.as_view(), name='logout')
]
