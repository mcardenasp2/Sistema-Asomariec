from django.forms import *


from proveedor.models import *

class ProveedorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['proEmpresa'].widget.attrs['autofocus'] = True

    class Meta:
        model= Proveedor
        fields='__all__'
        # exclude=['catFecReg','catFecMod']
        widgets={
            'proEmpresa':TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese el Nombre'
                }
            ),
            'proRuc': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Ruc',
                    'minlength': '10'
                }
            ),
            'proDireccion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la Dirección'
                }
            ),
            'proTelefono': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el N Telefónico',
                    'minlength': '10'
                }
            ),
            'proEmail': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Correo'
                }
            ),
            'provincia': Select(
                attrs={
                    'class': 'form-control mySelect2',
                    # 'placeholder': 'Ingrese el Correo'
                }
            ),
            'proDescripcion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la Descripcion de la Empresa'
                }
            )
        }

        exclude=['user_creation','user_updated']
        # widgets = {
        #     'catDescripcion': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese un nombre',
        #         }
        #     ),
        #     # 'desc': Textarea(
        #     #     attrs={
        #     #         'placeholder': 'Ingrese un nombre',
        #     #         'rows': 3,
        #     #         'cols': 3
        #     #     }
        #     # ),
        # }

    # solo cuando voy a enviar con ajax
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data



