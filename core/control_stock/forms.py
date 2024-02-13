from datetime import datetime

from django.forms import *
from django.forms.widgets import CheckboxInput

from core.control_stock.models import Categoria, ConversionMedida, Lote, Producto, SubCategoria, TipoOperacion, UnidadMedida

class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
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

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class SubCategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = SubCategoria
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'categoria': Select(),
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
    
    def clean(self):
        cleaned_data = super().clean()
        
class UnidadMedidaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = UnidadMedida
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'sigla': TextInput(
                attrs={
                    'placeholder': 'Ingrese una sigla',
                }
            ),
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

class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={'placeholder': 'Ingrese una descripción',}
            ),
            'categoria': Select(),
            'subcategoria': Select(),
            'tipo': Select(),
            'subtipo': Select(),
            'unidad_medida': Select(),
            'codigo_barra': TextInput(
                attrs={'placeholder': 'Ingrese un código de barra',}
            ),
            'codigo_fabrica': TextInput(
                attrs={'placeholder': 'Ingrese un código de fábrica',}
            ),
            'controla_lote': CheckboxInput(attrs={'class': 'required checkbox'}),
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

class LoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].widget.attrs['autofocus'] = True

    class Meta:
        model = Lote
        fields = '__all__'
        widgets = {
            'producto': Select(),
            'numero_lote': TextInput(
                attrs={
                    'placeholder': 'Ingrese un lote',
                }
            ),
            'fecha_elaboracion': DateInput(format='%Y-%m-%d',
                            attrs={
                                'value': datetime.now().strftime('%Y-%m-%d'),
                            }
            ),
            'fecha_vencimiento': DateInput(format='%Y-%m-%d',
                            attrs={
                                'value': datetime.now().strftime('%Y-%m-%d'),
                            }
            ),

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

class TipoOperacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = TipoOperacion
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
            'tipo': Select(),
            'afecta_costo': CheckboxInput(attrs={'class': 'required checkbox'}),
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
    
class ConversionMedidaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medida_de'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = ConversionMedida  # Cambia Lote a ConversionMedida
        fields = '__all__'
        widgets = {
            'medida_de': Select(),
            'medida_a': Select(),
            'operacion': Select(),
            'valor': TextInput(attrs={
                'class': 'form-control',
            }),
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
