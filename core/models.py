from django.db import models


class Producto(models.Model):
    CATEGORIA_CHOICES = [
        ('Laptops', 'Laptops'),
        ('Escritorio', 'Escritorio'),
        ('Perifericos', 'Perifericos'),
        ('Impresion', 'Impresion'),
        ('Almacenamiento', 'Almacenamiento'),
        ('Audio y Video', 'Audio y Video'),
        ('Mobiliario', 'Mobiliario'),
    ]

    sku = models.CharField(max_length=10, unique=True, verbose_name="SKU/Cod")
    nombre = models.CharField(max_length=120)
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES)
    costo_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

    @property
    def estado_stock(self):
        if self.stock < self.stock_minimo:
            return "Bajo Stock"
        elif self.stock < self.stock_minimo * 2:
            return "Moderado"
        return "Optimo"

    class Meta:
        ordering = ['sku']


class MovimientoStock(models.Model):
    TIPO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=150, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} - {self.cantidad}"

    class Meta:
        ordering = ['-fecha']

class MovimientoFinanciero(models.Model):
    TIPO_CHOICES = [
        ('Ingreso', 'Ingreso'),
        ('Gasto', 'Gasto'),
    ]
    MEDIO_PAGO_CHOICES = [
        ('Banco BHD', 'Banco BHD'),
        ('Caja Chica', 'Caja Chica'),
        ('Transferencia', 'Transferencia'),
        ('Efectivo', 'Efectivo'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateField()
    categoria = models.CharField(max_length=100)
    cliente_proveedor = models.CharField(max_length=120, verbose_name="Cliente / Proveedor")
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    medio_pago = models.CharField(max_length=20, choices=MEDIO_PAGO_CHOICES)
    factura = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.categoria} - RD$ {self.monto}"

    class Meta:
        ordering = ['-fecha']        