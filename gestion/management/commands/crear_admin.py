from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea un superusuario administrador si no existe'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@email.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Superusuario creado'))
        else:
            self.stdout.write(self.style.WARNING('El superusuario ya existe'))
        
