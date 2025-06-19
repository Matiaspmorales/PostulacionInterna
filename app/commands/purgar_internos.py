from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from app.models import PostulanteInterno

class Command(BaseCommand):
    help = 'Elimina postulantes internos con más de 6 meses de antigüedad.'

    def handle(self, *args, **options):
        # Umbral de 6 meses
        corte = timezone.now() - timedelta(days=180)
        total_borrados = 0

        # Sólo un modelo en la lista
        modelos = [PostulanteInterno]

        for modelo in modelos:
            query = modelo.objects.filter(fecha_creacion__lt=corte)
            cuenta = query.count()
            query.delete()
            self.stdout.write(f'  • {modelo.__name__}: {cuenta} borrados')
            total_borrados += cuenta

        self.stdout.write(self.style.SUCCESS(
            f'✅ Total eliminados: {total_borrados} postulaciones internas anteriores a {corte:%Y-%m-%d}'
        ))