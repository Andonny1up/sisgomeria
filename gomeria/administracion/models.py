from django.db import models


# clases basicas

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    ci = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()
    
    def __str__(self):
        return self.nombre + ' - ' + self.ci

class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    placa = models.CharField(max_length=7)
    
    def __str__(self):
        return self.placa

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    descipcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.nombre + ' - ' + self.marca + ' - ' + self.descipcion

# la siguiente clase es para el manejo de los servicios la cual llevara un registro de los servicios realizados en un vehiculo
class Servicio(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    pagado = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    productos = models.ManyToManyField(Producto, through='ServicioProducto')


class ServicioProducto(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=6, decimal_places=2) # precio del producto en el momento de la venta
    precio_total = models.DecimalField(max_digits=6, decimal_places=2) # precio por la cantidad de productos vendidos
    
    
    
class Pago(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=6, decimal_places=2)