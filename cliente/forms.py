from django.forms import *
from cliente.models import Cliente

class ClienteForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['cliEstado'].widget.attrs['class'] = 'custom-control-input'

    class Meta:
        model=Cliente
        fields = '__all__'

        widgets={
            'cliNombre': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un Nombre',
                }
            ),
            'cliApellido': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Apellido',
                }
            ),
            'cliRuc': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Ruc',
                    'minlength': '10'
                }
            ),
            'cliTelefono': TextInput(
                attrs={
                    'class': 'form-control phone',
                    'placeholder': 'Ingrese el Telefono',
                    'minlength':'10'
                }
            ),
            'cliDireccion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su Direccion',
                }
            ),
            'cliEmail': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'name@example.com',
                }
            ),
            # 'cliEstado': CheckboxInput(
            #     attrs={
            #         # 'class':'custom-control-input',
            #         'class':'form-check-input',
            #         # 'id':'customCheck1',
            #         # 'checked':'off'
            #
            #     }
            # ),

        }

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


