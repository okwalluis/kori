from datetime import datetime

from django.forms import *
from django.forms.widgets import CheckboxInput

from core.base.models import Deposito, Empresa, Pais, Persona, Sucursal

class PersonaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Persona
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese un apellido',
                }
            ),
            'razon_social': TextInput(
                attrs={
                    'placeholder': 'Ingrese una razón social',
                }
            ),
            'nombre_fantasia': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre de fantasía',
                }
            ),
            'tipo_persona': Select(),
            'fecha_nacimiento': DateInput(format='%d/%m/%Y',
                                       attrs={
                                           'value': datetime.now().strftime('%d/%m/%Y'),
                                       }
                                       ),
            'genero': Select(),
            'estado_civil': Select(),
            'activo': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
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

    def clean(self):
        cleaned_data = super().clean()
        tipo_persona = cleaned_data.get('tipo_persona')

        # Verificar el tipo de persona y hacer ajustes en función de ello
        if tipo_persona == 'F':
            # Para personas del tipo Fisico, el campo nombre_fantasia no es requerido
            cleaned_data['nombre_fantasia'] = ''
        else:
            cleaned_data['nombre'] = ''
            cleaned_data['apellido'] = ''
            cleaned_data['genero'] = ''
            cleaned_data['estado_civil'] = ''
        return cleaned_data

class EmpresaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Empresa
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'pais': Select(),
            'ruc': TextInput(
                attrs={
                    'placeholder': 'Ingrese un RUC válido',
                }
            ),
            'representante': Select(),
            'persona': Select(),
            'activo': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
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
    
    def clean(self):
        cleaned_data = super().clean()
        
class PaisForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Pais
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
            'activo': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
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

class SucursalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Sucursal
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una dirección',
                }
            ),
            'localidad': TextInput(
                attrs={
                    'placeholder': 'Ingrese una localidad',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese un teléfono',
                }
            ),
            'activo': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
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

class DepositoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Deposito
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'sucursal': Select(),
            'activo': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
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
