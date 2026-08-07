from django.core.management.base import BaseCommand
from core.models import Producto


class Command(BaseCommand):
    help = "Carga el catalogo inicial de productos de la tienda"

    def handle(self, *args, **kwargs):
        productos = [
            ("L001", "Laptop HP Pavilion 15\"", "Laptops", 22500, 22500, 15),
            ("L002", "Laptop Dell Inspiron 14\"", "Laptops", 19800, 19800, 12),
            ("L003", "Laptop Lenovo ThinkPad E14", "Laptops", 26000, 26000, 8),
            ("L004", "Laptop ASUS VivoBook 15\"", "Laptops", 18500, 18500, 10),
            ("L005", "MacBook Air M2", "Laptops", 58000, 58000, 5),
            ("D001", "PC Escritorio HP ProDesk", "Escritorio", 21000, 21000, 7),
            ("D002", "Monitor LG 24\" Full HD", "Escritorio", 6500, 6500, 20),
            ("D003", "Monitor Samsung 27\" Curvo", "Escritorio", 11200, 11200, 10),
            ("D004", "Monitor Dell 22\"", "Escritorio", 5800, 5800, 18),
            ("D005", "All-in-One HP 24\"", "Escritorio", 28000, 28000, 6),
            ("P001", "Teclado Mecanico Logitech", "Perifericos", 3200, 3200, 25),
            ("P002", "Mouse Inalambrico Logitech M170", "Perifericos", 650, 650, 40),
            ("P003", "Combo Teclado y Mouse HP", "Perifericos", 1200, 1200, 30),
            ("P004", "Mouse Gamer Redragon", "Perifericos", 1450, 1450, 22),
            ("P005", "Teclado Numerico USB", "Perifericos", 550, 550, 35),
            ("I001", "Impresora HP DeskJet 2775", "Impresion", 5900, 5900, 10),
            ("I002", "Impresora Epson EcoTank L3250", "Impresion", 9800, 9800, 8),
            ("I003", "Cartucho De Tinta HP 664 Negro", "Impresion", 850, 850, 45),
            ("I004", "Cartucho De Tinta Epson 664 Color", "Impresion", 920, 920, 38),
            ("I005", "Toner HP 85A", "Impresion", 3600, 3600, 14),
            ("A001", "Disco Duro Externo Seagate 1TB", "Almacenamiento", 3100, 3100, 20),
            ("A002", "SSD Kingston 480GB", "Almacenamiento", 2400, 2400, 25),
            ("A003", "Memoria USB SanDisk 32GB", "Almacenamiento", 450, 450, 60),
            ("A004", "Memoria RAM Kingston 8GB DDR4", "Almacenamiento", 2100, 2100, 30),
            ("A005", "Cargador Universal Laptop", "Almacenamiento", 1300, 1300, 28),
            ("V001", "Webcam Logitech C270", "Audio y Video", 1800, 1800, 18),
            ("V002", "Audifonos Con Microfono HyperX", "Audio y Video", 3400, 3400, 16),
            ("V003", "Bocinas USB Logitech", "Audio y Video", 1100, 1100, 24),
            ("V004", "Diadema Bluetooth JBL", "Audio y Video", 4200, 4200, 12),
            ("M001", "Silla Ergonomica Oficina", "Mobiliario", 8500, 8500, 9),
            ("M002", "Escritorio Para Computadora", "Mobiliario", 7200, 7200, 11),
            ("M003", "Base Para Laptop Ajustable", "Mobiliario", 950, 950, 20),
        ]

        creados = 0
        for sku, nombre, categoria, costo, precio, stock in productos:
            obj, fue_creado = Producto.objects.get_or_create(
                sku=sku,
                defaults={
                    "nombre": nombre,
                    "categoria": categoria,
                    "costo_compra": costo,
                    "precio_venta": precio,
                    "stock": stock,
                }
            )
            if fue_creado:
                creados += 1

        self.stdout.write(self.style.SUCCESS(f"Listo. Se crearon {creados} productos nuevos."))