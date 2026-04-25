from django import forms
from .models import Herramienta, Usuario, Prestamo,Mantenimiento


class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = [
            'nombre',
            'marca',
            'modelo',
            'numero_serie',
            'estado',
            'id_categoria',
        ]

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'correo',
            'telefono',
            'area',
            'id_rol',
        ]

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            'fecha_prestamo',
            'fecha_devolucion',
            'fecha_entrega_real',
            'estado_prestamo',
            'id_usuario',
            'id_herramienta',
        ]

        widgets = {
            'fecha_prestamo': forms.DateInput(attrs={'type': 'date'}),
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_entrega_real': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        herramienta = cleaned_data.get('id_herramienta')
        estado_prestamo = cleaned_data.get('estado_prestamo')
        fecha_prestamo = cleaned_data.get('fecha_prestamo')
        fecha_devolucion = cleaned_data.get('fecha_devolucion')
        fecha_entrega_real = cleaned_data.get('fecha_entrega_real')

        if herramienta and estado_prestamo == 'Prestado' and herramienta.estado != 'Disponible':
            raise forms.ValidationError('No se puede prestar una herramienta que no este prestada o en mantención.')

        if fecha_prestamo and fecha_devolucion and fecha_devolucion < fecha_prestamo:
            raise forms.ValidationError('La fecha de devolución no puede ser anterior a la fecha de préstamo.')

        if fecha_prestamo and fecha_entrega_real and fecha_entrega_real < fecha_prestamo:
            raise forms.ValidationError('La fecha de entrega real no puede ser anterior a la fecha de préstamo.')

        return cleaned_data

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = [
            'fecha_mantenimiento',
            'tipo_mantenimiento',
            'descripcion',
            'id_herramienta',
        ]

        widgets = {
            'fecha_mantenimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        herramienta = cleaned_data.get('id_herramienta')

        if herramienta and herramienta.estado != 'Disponible':
            raise forms.ValidationError('Solo se puede registrar mantenimiento para herramientas disponibles.')

        return cleaned_data