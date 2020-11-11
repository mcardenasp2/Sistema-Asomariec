from datetime import datetime

from django.forms import *
from venta.models import *


class CabVentaForm(ModelForm):
    # medida=ModelChoiceField(queryset=UnidadMedidad.objects.filter(medEstado=1))
    # categoria=ModelChoiceField(queryset=Categoria.objects.filter(catEstado=1))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        # self.fields['medDescripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Venta
        fields = '__all__'
        # exclude=['catFecReg','catFecMod']
        widgets = {
            'cliente': Select(
                # format='%Y-%m-%d',
                attrs={
                    'class': 'form-control mySelect2',
                    # 'placeholder':'Ingrese un Cliente'
                    # 'value': datetime.now().strftime('%Y-%m-%d'),
                    # 'autocomplete': 'off',
                    # 'class': 'form-control datetimepicker-input',
                    # 'id': 'ccoFecCom',
                    # 'data-target': '#ccoFecCom ',
                    # 'data-toggle': 'datetimepicker'
                }
            ),
            'venFechaInici': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'venFechaInici',
                    'data-target': '#venFechaInici ',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'venFechaFin': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'venFechaFin',
                    'data-target': '#venFechaFin ',
                    'data-toggle': 'datetimepicker'
                }
            ),

        }

