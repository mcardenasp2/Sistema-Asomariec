from django.db.models import Q
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
                    'autocomplete':'off'
                }
            ),
            'cliApellido': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Apellido',
                    'autocomplete':'off'
                }
            ),
            'cliRuc': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Ruc',
                    'minlength': '10',
                    'autocomplete': 'off'
                }
            ),
            'cliTelefono': TextInput(
                attrs={
                    'class': 'form-control phone',
                    'placeholder': 'Ingrese el Telefono',
                    'minlength':'10',
                    'autocomplete': 'off'
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
                    'autocomplete': 'off'
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

        exclude=['user_creation','user_updated']

    def comprobar(self):

        # print(self.cleaned_data['cliEmail'])
        # email = self.cleaned_data['cliEmail']

        email = self.cleaned_data['cliEmail']
        ruc = self.cleaned_data['cliRuc']
        resp = Cliente.objects.get(Q(cliEmail=email) | Q(cliRuc=ruc), cliEstado=True, id=1)
        print(resp.id)
        if resp is None:
            print("Guardar")
            # instance = form.save()
            # data = instance.toJSON()
        else:
            if resp.id:
                print("Editar")
                # instance = form.save()
                # data = instance.toJSON()
            else:
                if resp.cliEmail == email:
                    print("Email existe")
                if resp.cliRuc == ruc:
                    print("Email existe")
        return resp;

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# class ContratoForm(ModelForm):
#     class Meta:
#         model=Contrato
#         fields='__all__'
#         widgets={
#             'contratoDescripcion': TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     # 'placeholder': 'Ingrese un Nombre',
#                     # 'autocomplete':'off'
#                 }
#             )
#         }

