from datetime import datetime

from django.forms import *
from venta.models import *
from cliente.models import Cliente


class CabVentaForm(ModelForm):
    cliente = ModelChoiceField(queryset=Cliente.objects.filter(cliEstado=1))
    # medida=ModelChoiceField(queryset=UnidadMedidad.objects.filter(medEstado=1))
    # categoria=ModelChoiceField(queryset=Categoria.objects.filter(catEstado=1))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cliente'] = ModelChoiceField(queryset=Cliente.objects.filter(cliEstado=1))
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        # self.fields['medDescripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Venta
        fields = '__all__'
        # exclude=['catFecReg','catFecMod']
        widgets = {
            # 'cliente': Select(
            #     # format='%Y-%m-%d',
            #     attrs={
            #         'class': 'form-control mySelect2',
            #     }
            # ),
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

