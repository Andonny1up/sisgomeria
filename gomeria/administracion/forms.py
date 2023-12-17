from django import forms
from .models import Cliente, Vehiculo, Producto, Servicio, Pago

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'ci', 'telefono', 'direccion', 'email']

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'marca', 'modelo', 'placa']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'descipcion', 'precio']

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['vehiculo', 'fecha', 'descripcion', 'precio', 'pagado', 'total', 'productos']

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['servicio', 'fecha', 'monto']