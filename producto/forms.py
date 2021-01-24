from django.forms import *

from producto.models import *


class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prodDescripcion'].widget.attrs['autofocus'] = True


    class Meta:
        model= Producto
        fields='__all__'
        widgets = {
            'prodCaracteristica': Textarea(
                attrs={
                    'class': 'form-control',
                    'rows':3
                },

            ),
            'prodDescripcion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese el Nombre',
                    # 'autofocus':True
                },

            ),
            'prodCantidad': TextInput(
                attrs={
                    'class': 'form-control',
                    'disabled':'disabled'
                },
            ),
            'prodPrecio': TextInput(
                attrs={
                    'class': 'form-control',
                },
            ),
            'prodIva': TextInput(
                attrs={
                    'class': 'form-control',
                    'value':0.12
                },
            ),
            'prodTotal': TextInput(
                attrs={
                    'class': 'form-control',
                    'disabled': 'disabled'
                },
            ),
        }
        # exclude=['catFecReg','catFecMod']


    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                # print(form.fields)
                # guarda ruta de insumo
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data