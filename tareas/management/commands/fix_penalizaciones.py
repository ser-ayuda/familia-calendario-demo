from decimal import Decimal
from django.core.management.base import BaseCommand
from tareas.models import Reto

class Command(BaseCommand):
    help = 'Corrige penalizaciones no numéricas en los retos.'

    def handle(self, *args, **options):
        self.stdout.write('Corrigiendo penalizaciones no numéricas en los retos...')
        count = 0
        for reto in Reto.objects.all():
            try:
                float(reto.penalizacion)
            except Exception:
                reto.penalizacion = Decimal('0.00')
                reto.save()
                count += 1
        self.stdout.write(f'Penalizaciones corregidas: {count}')
