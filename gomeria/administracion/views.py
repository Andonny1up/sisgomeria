from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Cliente, Vehiculo, Producto, Servicio, Pago
from .forms import ClienteForm, VehiculoForm, ProductoForm, ServicioForm, PagoForm
from django.shortcuts import render
from django.urls import reverse_lazy

#VISTA INICIO
def home(request):
    return render(request, 'administracion/home.html',{})

# vista lista de clientes
class ClienteListView(ListView):
    model = Cliente
    template_name = 'administracion/clientes/browse.html'
    context_object_name = 'clientes'
    
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'administracion/clientes/create.html'
    success_url = reverse_lazy('administracion:clientes')

class VehiculoCreateView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'nombre_template.html'
    success_url = '/donde_redirigir_despues_de_crear'

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'nombre_template.html'
    success_url = '/donde_redirigir_despues_de_crear'

class ServicioCreateView(CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'nombre_template.html'
    success_url = '/donde_redirigir_despues_de_crear'

class PagoCreateView(CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'nombre_template.html'
    success_url = '/donde_redirigir_despues_de_crear'