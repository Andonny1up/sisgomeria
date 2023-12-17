from django.urls import path
from . import views
from .views import ClienteCreateView, VehiculoCreateView, ProductoCreateView, ServicioCreateView, PagoCreateView

app_name = 'administracion'

urlpatterns = [
    path('', views.home, name='home'),
    path('clientes/', views.ClienteListView.as_view(), name='clientes'),
    path('clientes/crear/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='detalle_cliente'),
    
    path('crear_vehiculo/', VehiculoCreateView.as_view(), name='crear_vehiculo'),
    
    path('productos/', views.ProductoListView.as_view(), name='productos'),
    path('productos/crear', ProductoCreateView.as_view(), name='crear_producto'),
    
    path('servicios/', views.ServicioListView.as_view(), name='servicios'),
    path('servicios/crear', ServicioCreateView.as_view(), name='crear_servicio'),
    
    path('crear_pago/', PagoCreateView.as_view(), name='crear_pago'),
]