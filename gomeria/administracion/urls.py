from django.urls import path
from . import views
from .views import ClienteCreateView, VehiculoCreateView, ProductoCreateView, PagoCreateView

app_name = 'administracion'

urlpatterns = [
    path('', views.home, name='home'),
    path('clientes/', views.ClienteListView.as_view(), name='clientes'),
    path('clientes/crear/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='detalle_cliente'),
    path('buscar_cliente/', views.BuscarClienteView.as_view(), name='buscar_cliente'),
    
    path('crear_vehiculo/', VehiculoCreateView.as_view(), name='crear_vehiculo'),
    path('get_vehiculos/', views.GetVehiculosView.as_view(), name='get_vehiculos'),
    
    path('productos/', views.ProductoListView.as_view(), name='productos'),
    path('productos/crear', ProductoCreateView.as_view(), name='crear_producto'),
    
    path('servicios/', views.ServicioListView.as_view(), name='servicios'),
    path('servicios/crear', views.create_servicio, name='crear_servicio'),
    path('servicios/<int:servicio_id>/factura', views.factura, name='servicio_factura'),
    
    path('pagos/<int:servicio_id>/crear',views.realizar_pago , name='crear_pago'),
]