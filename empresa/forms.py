from django.forms import *
from empresa.models import Empresa

class EmpresaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emprNombre'].widget.attrs['autofocus'] = True

    class Meta:
        model=Empresa
        fields = '__all__'

        widgets={
            'emprNombre': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un Nombre',
                    'autocomplete':'off'
                }
            ),

            'emprRuc': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Ruc',
                    'minlength': '10',
                    'autocomplete': 'off'
                }
            ),
            'emprTelefono': TextInput(
                attrs={
                    'class': 'form-control phone',
                    'placeholder': 'Ingrese el Telefono',
                    'minlength':'10',
                    'autocomplete': 'off'
                }
            ),
            'emprDireccion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su Direccion',
                }
            ),
            'emprEmail': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'name@example.com',
                    'autocomplete': 'off'
                }
            ),

        }

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
