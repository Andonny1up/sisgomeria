from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
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
    

class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'administracion/clientes/detail.html'
    context_object_name = 'cliente'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehiculo_form'] = VehiculoForm(initial={'cliente': self.object})
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = VehiculoForm(request.POST)
        
        if form.is_valid():
            form.save()
        
        return self.get(request, *args, **kwargs)

class VehiculoCreateView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'nombre_template.html'
    success_url = '/donde_redirigir_despues_de_crear'


class ProductoListView(ListView):
    model = Producto
    template_name = 'administracion/productos/list.html'
    context_object_name = 'productos'
    
    
class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'administracion/productos/create.html'
    success_url = reverse_lazy('administracion:productos')


class ServicioListView(ListView):
    model = Servicio
    template_name = 'administracion/servicios/list.html'
    context_object_name = 'servicios'
    

class ServicioCreateView(CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'administracion/servicios/create.html'
    success_url = reverse_lazy('administracion:servicios')

class PagoCreateView(CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'nombre_template.html'
    success_url = '/donde_redirigir_despues_de_crear'