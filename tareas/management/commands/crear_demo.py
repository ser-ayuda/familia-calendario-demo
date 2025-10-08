from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Crea el usuario demo si no existe'

    def handle(self, *args, **options):
        if not User.objects.filter(username='demo').exists():
            User.objects.create_user('demo', password='demo')
            self.stdout.write(self.style.SUCCESS('Usuario demo creado'))
        else:
            self.stdout.write(self.style.WARNING('El usuario demo ya existe'))
