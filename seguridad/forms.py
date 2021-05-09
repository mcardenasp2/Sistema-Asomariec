from django.forms import *
from seguridad.models import Modulo, ModuloGrupo

from django.contrib.auth.models import Group

class ModuloForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model=Modulo
        fields = '__all__'

        widgets={
            'url': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese Url',
                    'autocomplete':'off'
                }
            ),

            'nombre': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Nombre',
                    # 'minlength': '10',
                    'autocomplete': 'off'
                }
            ),
            'icono': TextInput(
                attrs={
                    'class': 'form-control phone',
                    'placeholder': 'Ingrese el Icono',
                    # 'minlength':'10',
                    'autocomplete': 'off'
                }
            ),
            'descripcion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la Descripción',
                }
            ),
            # 'activo': TextInput(
            #     attrs={
            #         'class': 'form-control',
            #         # 'placeholder': 'name@example.com',
            #         'autocomplete': 'off'
            #     }
            # ),
            'orden': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el orden',
                    'autocomplete': 'off'
                }
            ),

        }
        exclude=['activo']


    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance=form.save()
                # data=instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data



class GrupoModuloForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modulos'].queryset = Modulo.objects.filter(activo=True)
        # self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ModuloGrupo
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'icono': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Icono',
                }
            ),
            'descripcion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su email',
                }
            ),
            'prioridad': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su username',
                }
            ),

            'grupos': SelectMultiple(attrs={
                'class': 'form-control select2',
                # 'style': 'width: 100%',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }),

            'modulos': SelectMultiple(attrs={
                'class': 'form-control select2',
                # 'style': 'width: 100%',
                'style': 'width: 100%',
                'multiple': 'multiple'
            })

            # 'groups': SelectMultiple(attrs={
            #     'class': 'form-control select2',
            #     # 'style': 'width: 100%',
            #     'style': 'width: 100%',
            #     'multiple': 'multiple'
            # })
        }
        exclude=['activo']
        # exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                # pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                # if u.pk is None:
                #     u.set_password(pwd)
                # else:
                #     user = User.objects.get(pk=u.pk)
                #     if user.password != pwd:
                #         u.set_password(pwd)
                u.save()
                u.grupos.clear()
                u.modulos.clear()
                # puse para eliminar la sesion

                for g in self.cleaned_data['grupos']:
                    u.grupos.add(g)
                for g in self.cleaned_data['modulos']:
                    u.modulos.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data




class GrupoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Nombre del Rol',
                }
            ),
            # 'icono': TextInput(
            #     attrs={
            #         'class': 'form-control',
            #         'placeholder': 'Ingrese el Icono',
            #     }
            # ),
            # 'descripcion': TextInput(
            #     attrs={
            #         'class': 'form-control',
            #         'placeholder': 'Ingrese su email',
            #     }
            # ),
            # 'prioridad': TextInput(
            #     attrs={
            #         'class': 'form-control',
            #         'placeholder': 'Ingrese su username',
            #     }
            # ),

            'permissions': SelectMultiple(attrs={
                'class': 'form-control select2',
                # 'style': 'width: 100%',
                'style': 'width: 100%; height:350px',
                'multiple': 'multiple'
            }),

            # 'modulos': SelectMultiple(attrs={
            #     'class': 'form-control select2',
            #     # 'style': 'width: 100%',
            #     'style': 'width: 100%',
            #     'multiple': 'multiple'
            # })

            # 'groups': SelectMultiple(attrs={
            #     'class': 'form-control select2',
            #     # 'style': 'width: 100%',
            #     'style': 'width: 100%',
            #     'multiple': 'multiple'
            # })
        }
        # exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                # pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                # if u.pk is None:
                #     u.set_password(pwd)
                # else:
                #     user = User.objects.get(pk=u.pk)
                #     if user.password != pwd:
                #         u.set_password(pwd)
                u.save()
                u.permissions.clear()
                # u.modulos.clear()
                # puse para eliminar la sesion

                for g in self.cleaned_data['permissions']:
                    u.permissions.add(g)
                # for g in self.cleaned_data['modulos']:
                #     u.modulos.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data