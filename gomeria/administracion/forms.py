from django import forms
from .models import Cliente, Vehiculo, Producto, Servicio, Pago, ServicioProducto
from django.forms import formset_factory


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'ci', 'telefono', 'direccion', 'email']

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'marca', 'modelo', 'placa']
        widgets = {
            'cliente': forms.HiddenInput(),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'descipcion', 'precio']

class ServicioForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), empty_label="Seleccione cliente")
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.none(), empty_label=None)
    
    class Meta:
        model = Servicio
        fields = ['cliente','vehiculo', 'descripcion', 'precio', 'productos']
        

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['servicio', 'fecha', 'monto']