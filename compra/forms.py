from django.forms import *
from compra.models import *


class CabCompraForm(ModelForm):
    # medida=ModelChoiceField(queryset=UnidadMedidad.objects.filter(medEstado=1))
    # categoria=ModelChoiceField(queryset=Categoria.objects.filter(catEstado=1))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        # self.fields['medDescripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = CabCompra
        fields = '__all__'
        # exclude=['catFecReg','catFecMod']
        widgets = {
            'ccoFecCom': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'ccoFecCom',
                    'data-target': '#ccoFecCom ',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'proveedor':Select(
                attrs={
                    'class':'form-control mySelect2'
                }
            ),
            'ccoIva': TextInput(
                attrs={
                    'class': 'form-control',
                    'type':'hidden'
                }
            ),
            'ccoVendedor': TextInput(
                attrs={
                    'class': 'form-control',

                }
            ),
            'ccoCedVend': TextInput(
                attrs={
                    'class': 'form-control',
                    'minlength': '10'
                }
            ),

            #     'medDescripcion': TextInput(
            #         attrs={
            #             'placeholder': 'Ingrese un nombre',
            #         }
            #     ),
            # 'desc': Textarea(
            #     attrs={
            #         'placeholder': 'Ingrese un nombre',
            #         'rows': 3,
            #         'cols': 3
            #     }
            # ),
        }

    # solo cuando voy a enviar con ajax
    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             # print(form.fields)
    #             # guarda ruta de insumo
    #             form.save()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data
