from django.forms import *

from producto.models import *

class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
                },

            ),
            'prodCantidad': TextInput(
                attrs={
                    'class': 'form-control',
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