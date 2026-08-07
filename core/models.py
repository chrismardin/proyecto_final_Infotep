from django.db import models
from django.utils import timezone


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
        return "Óptimo"

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
    fecha = models.DateField(default=timezone.now)  # 👈 ahora tiene valor por defecto
    categoria = models.CharField(max_length=100)
    cliente_proveedor = models.CharField(max_length=120, verbose_name="Cliente / Proveedor", blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    medio_pago = models.CharField(max_length=20, choices=MEDIO_PAGO_CHOICES, blank=True)
    factura = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.categoria} - RD$ {self.monto}"

    class Meta:
        ordering = ['-fecha']


class ProductoVentaHistorial(models.Model):
    """
    Guarda los productos que se han usado alguna vez en el formulario
    de Ventas, para poder reutilizarlos rapido (pestaña "Historial"
    de la pagina de Ventas). Antes esto vivia en localStorage; ahora
    se guarda en la base de datos para que no se pierda al recargar
    la pagina ni al cambiar de computadora.
    """
    sku = models.CharField(max_length=20, unique=True, verbose_name="SKU/Cod")
    nombre = models.CharField(max_length=120)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

    class Meta:
        ordering = ['nombre']
