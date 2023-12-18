from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Cliente, Vehiculo, Producto, Servicio, Pago
from .forms import ClienteForm, VehiculoForm, ProductoForm, ServicioForm, PagoForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404

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
    

class BuscarClienteView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        clientes = Cliente.objects.filter(Q(nombre__icontains=q) | Q(ci__icontains=q))[:20]
        results = [{'id': cliente.id, 'text': f'{cliente.nombre}'} for cliente in clientes]
        return JsonResponse({'results': results})


class VehiculoCreateView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'nombre_template.html'
    success_url = '/donde_redirigir_despues_de_crear'
    
class GetVehiculosView(View):
    def get(self, request, *args, **kwargs):
        cliente_id = request.GET.get('cliente_id')
        vehiculos = Vehiculo.objects.filter(cliente_id=cliente_id).values('id', 'placa')
        return JsonResponse(list(vehiculos), safe=False)

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
    

class PagoCreateView(CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'nombre_template.html'
    success_url = '/donde_redirigir_despues_de_crear'
    
    
def create_servicio(request):
    if request.method == 'POST':
        # recoger los datos del formulario
        vehiculo_id = request.POST.get('vehiculo')
        
        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        productos = request.POST.getlist('producto[]')
        cantidades = request.POST.getlist('cantidad[]')
        
        # crear el servicio
        servicio = Servicio.objects.create(
            vehiculo=vehiculo,
            descripcion=descripcion,
            precio=precio,
            total=0,
            fecha=timezone.now(),
        )
        servicio.save()
        #añadir productos si existen
        if len(productos) > 0:
            for i, producto_id in enumerate(productos):
                producto = Producto.objects.get(id=producto_id)
                cantidad = cantidades[i]
                precio_total = producto.precio * int(cantidad)
                servicio.productos.add(producto, through_defaults={'cantidad': cantidad, 'precio': producto.precio, 'precio_total': precio_total})
        
        # calcular el total del servicio
        total = 0.0
        for item in servicio.productos.through.objects.filter(servicio=servicio):
            total += float(item.precio_total)
            print(item.precio_total)
            print(total)
        
        total += float(servicio.precio)
        
        # actualizar el total del servicio
        servicio.total = total
        servicio.save()
        
        # redirigir a la lista de servicios
        return redirect('administracion:servicios')
    else:
        productos = Producto.objects.all()
        return render(request, 'administracion/servicios/create.html', {
            'productos': productos,
        })
        
        
def realizar_pago(request,servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    
    if request.method == 'POST':
        monto = float(request.POST.get('monto'))
        fecha = timezone.now()
        
        #comprobar que el monto no sea mayor al total del servicio
        total_pagado = sum(pago.monto for pago in servicio.pago_set.all())
        if float(total_pagado) + monto > servicio.total:
            return render(request, 'administracion/pagos/create.html', {
                'servicio': servicio,
                'error': 'El monto ingresado es mayor al total del servicio',
            })
        else:
            pago = Pago.objects.create(
                servicio=servicio,
                monto=monto,
                fecha=fecha,
            )
            pago.save()
            #comprobar si el servicio ya fue pagado totalmente
            total_pagado = sum(pago.monto for pago in servicio.pago_set.all())
            if total_pagado == servicio.total:
                servicio.pagado = True
                servicio.save()
            
            return redirect('administracion:servicios')
    else:
        total_pagado = sum(pago.monto for pago in servicio.pago_set.all())
        faltante = servicio.total - total_pagado
        return render(request, 'administracion/pagos/create.html', {
            'servicio': servicio,
            'faltante': faltante,
        })
        

def factura(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    items = servicio.productos.through.objects.filter(servicio=servicio)
    return render(request, 'administracion/servicios/factura.html', {
        'servicio': servicio,
        'items': items,
    })