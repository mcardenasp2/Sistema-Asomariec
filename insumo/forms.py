from django.forms import *


from insumo.models import *

class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['catDescripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model= Categoria
        fields='__all__'
        # exclude=['catFecReg','catFecMod']
        widgets = {
            'catDescripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            # 'desc': Textarea(
            #     attrs={
            #         'placeholder': 'Ingrese un nombre',
            #         'rows': 3,
            #         'cols': 3
            #     }
            # ),
        }

        exclude=['user_creation','user_updated']

    # solo cuando voy a enviar con ajax
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

class MedidaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['medDescripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model= UnidadMedidad
        fields='__all__'
        # exclude=['catFecReg','catFecMod']
        widgets = {
            'medDescripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            # 'desc': Textarea(
            #     attrs={
            #         'placeholder': 'Ingrese un nombre',
            #         'rows': 3,
            #         'cols': 3
            #     }
            # ),
        }

        exclude=['user_updated','user_creation']

    # solo cuando voy a enviar con ajax
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

class InsumoForm(ModelForm):
    medida=ModelChoiceField(queryset=UnidadMedidad.objects.filter(medEstado=1))
    categoria=ModelChoiceField(queryset=Categoria.objects.filter(catEstado=1))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['insDescripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model= Insumo
        fields='__all__'
        # exclude=['catFecReg','catFecMod']
        widgets = {
            'insStock': TextInput(
                    attrs={
                        'class':'form-control',
                        'required': False,
                        'disabled':'disabled'
                        # 'placeholder': 'Ingre,
                    },


                ),
            'insPrecio': TextInput(

                attrs={
                    'class': 'form-control',
                    # 'value':'1',

                    # 'data-mask' : '00/00/0000'
                    # 'disabled': 'disabled'
                    # 'placeholder': 'Ingre',
                },


            ),
            'insIva': TextInput(

                attrs={
                    'class': 'form-control',
                    # 'value':'1',

                    # 'data-mask' : '00/00/0000'
                    # 'disabled': 'disabled'
                    # 'placeholder': 'Ingre',
                },

            ),
            'insCod': TextInput(
                attrs={
                    'class': 'form-control',
                    # 'value':'0.jh00'
                    # 'data-mask' : '00/00/0000'
                    # 'disabled': 'disabled'
                    'placeholder': 'Ingrese el Codigo',
                },

            ),
            'insModelo': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Modelo',
                },

            ),
            'insDescripcion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Nombre',
                },

            ),
        }

        exclude=['user_updated','user_creation']
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
        # }

    # solo cuando voy a enviar con ajax
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



