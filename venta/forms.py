from datetime import datetime
from django import forms
from django.forms import ModelForm
from venta.models import *
from cliente.models import *


class CabVentaForm(ModelForm):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'title': 'Desde  -  Hasta',
        # 'id':'date_ran'
    }))
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(cliEstado=1))
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
            'venFechaInici': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'venFechaInici',
                    'data-target': '#venFechaInici',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'venFechaFin': forms.DateInput(
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
            'venEstVenta':forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

        }

