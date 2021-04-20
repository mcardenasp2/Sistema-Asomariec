from django.forms import *

from producto.models import *


class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['catDescripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'catDescripcion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de Categoria',
                }
            )

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


class ProductoForm(ModelForm):
    categoria = ModelChoiceField(queryset=Categoria.objects.filter(catEstado=1))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prodDescripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'prodCaracteristica': Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                },

            ),
            'prodDescripcion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Nombre',
                    # 'autofocus':True
                },

            ),
            'prodCantidad': TextInput(
                attrs={
                    'class': 'form-control',
                    'disabled': 'disabled'
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
                    'value': 0.12
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


class ProduccionForm(ModelForm):
    # producto = ModelChoiceField(queryset=Producto.objects.filter(prodEstado=1))
    # producto = ModelChoiceField(queryset=Producto.objects.filter(prodEstado=1, prodTipo=2, prodEstprod=1))
    producto = ModelChoiceField(queryset=Producto.objects.filter(prodEstado=1, prodTipo=2))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Produccion
        fields = '__all__'
        widgets = {

            'prodcFecElab': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'prodcFecElab',
                    'data-target': '#prodcFecElab',
                    'data-toggle': 'datetimepicker'
                }
            ),

            'prodcCantidad': TextInput(
                attrs={
                    'class': 'form-control',
                    # 'disabled':'disabled'
                },
            ),

            'prodcTotal': TextInput(
                attrs={
                    'class': 'form-control',
                    'disabled': 'disabled'
                },
            ),
        }
        # exclude=['catFecReg','catFecMod']
