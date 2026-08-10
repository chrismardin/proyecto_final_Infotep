from django.core.management.base import BaseCommand
from core.models import Cliente


class Command(BaseCommand):
    help = "Carga clientes de ejemplo"

    def handle(self, *args, **kwargs):
        clientes = [
            ("Publico", "", "", "Publico"),
            ("Jose Gutierrez", "Acero Estrella", "809-468-8255", "Empresa"),
            ("Juan Mendez", "Cecomsa", "809-400-8785", "Empresa"),
            ("Rosa Peña", "", "809-555-1023", "Frecuente"),
            ("Francisco Ventura", "", "809-555-2045", "Frecuente"),
        ]

        creados = 0
        for nombre, empresa, telefono, tipo in clientes:
            obj, fue_creado = Cliente.objects.get_or_create(
                nombre=nombre,
                defaults={"empresa": empresa, "telefono": telefono, "tipo": tipo}
            )
            if fue_creado:
                creados += 1

        self.stdout.write(self.style.SUCCESS(f"Listo. Se crearon {creados} clientes nuevos."))