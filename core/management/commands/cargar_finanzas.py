from django.core.management.base import BaseCommand
from core.models import MovimientoFinanciero
from datetime import date


class Command(BaseCommand):
    help = "Carga movimientos financieros de ejemplo"

    def handle(self, *args, **kwargs):
        movimientos = [
            ("Ingreso", date(2026, 6, 17), "Venta Laptop", "Rosa Peña", 43250.00, "Banco BHD", "F000001"),
            ("Ingreso", date(2026, 6, 15), "Venta Impresora", "Crismardin Castaño", 23000.00, "Caja Chica", "F000025"),
            ("Ingreso", date(2026, 6, 10), "Servicio Consultoria", "Francisco Ventura", 26000.00, "Caja Chica", "F000019"),
            ("Gasto", date(2026, 6, 17), "Pago Luz", "EDENORTE", 35220.00, "Banco BHD", ""),
            ("Gasto", date(2026, 6, 2), "Compra Stock", "Proveedor Tech RD", 1880.00, "Caja Chica", ""),
            ("Gasto", date(2026, 1, 25), "Compra Stock", "Proveedor Tech RD", 880.00, "Caja Chica", ""),
            ("Gasto", date(2026, 7, 22), "Compra Stock", "Proveedor Tech RD", 250.00, "Banco BHD", ""),
        ]

        creados = 0
        for tipo, fecha, categoria, cliente, monto, medio, factura in movimientos:
            obj, fue_creado = MovimientoFinanciero.objects.get_or_create(
                tipo=tipo, fecha=fecha, categoria=categoria, cliente_proveedor=cliente,
                defaults={
                    "monto": monto,
                    "medio_pago": medio,
                    "factura": factura,
                }
            )
            if fue_creado:
                creados += 1

        self.stdout.write(self.style.SUCCESS(f"Listo. Se crearon {creados} movimientos nuevos."))