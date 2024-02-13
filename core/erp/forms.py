from datetime import datetime

from django.forms import *

from core.erp.models import CabMovimiento, Caja, Category, Concepto, Moneda, Product, Client, Sale


class ConceptoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Concepto
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                }
            ),
            'tipo': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'activo': CheckboxInput(attrs={'class': 'required checkbox'}),
        }
        exclude = ['empresa','created_by', 'modified_by']

    def save(self, commit=True, empresa_id=None):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form = super().save(commit=False)
                form.empresa_id = empresa_id
                if commit:
                    form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class MonedaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Moneda
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                }
            ),
            'sigla': TextInput(
                attrs={
                    'placeholder': 'Ingrese una sigla',
                }
            ),
            #'cantidad_decimales': TextInput(attrs={
            #    'class': 'form-control',
            #}),
            'activo': CheckboxInput(attrs={'class': 'required checkbox'}),
        }
        exclude = ['created_by', 'modified_by']

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

class CajaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Caja
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                }
            ),
            'tipo': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'moneda': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'activo': CheckboxInput(attrs={'class': 'required checkbox'}),
        }
        exclude = ['empresa','created_by', 'modified_by']
        
    def save(self, commit=True, empresa_id=None):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form = super().save(commit=False)
                form.empresa_id = empresa_id
                if commit:
                    form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class CabMovimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CabMovimiento
        fields = '__all__'
        widgets = {
            'tipo_operacion': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'numero': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'fecha': DateInput(
                format='%d-%m-%Y',
                attrs={
                    'value': datetime.now().strftime('%d-%m-%Y'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'deposito': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'observacion': TextInput(attrs={
                'class': 'form-control',
            }),
            'activo': CheckboxInput(attrs={'class': 'required checkbox'}),
        }


class TestForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }
