from django.core.management.base import BaseCommand
from tareas.models import Aviso
import csv

class Command(BaseCommand):
    help = 'Exporta los avisos administrativos a un archivo CSV.'

    def add_arguments(self, parser):
        parser.add_argument('--output', type=str, default='avisos_export.csv', help='Ruta del archivo de salida CSV')
        parser.add_argument('--usuario', type=str, help='Filtrar por nombre de usuario')
        parser.add_argument('--desde', type=str, help='Fecha inicial (YYYY-MM-DD)')
        parser.add_argument('--hasta', type=str, help='Fecha final (YYYY-MM-DD)')

    def handle(self, *args, **options):
        from django.utils.dateparse import parse_date
        output_path = options['output']
        avisos = Aviso.objects.select_related('usuario').all()
        # Filtro por usuario
        if options.get('usuario'):
            avisos = avisos.filter(usuario__username=options['usuario'])
        # Filtro por fecha inicial
        if options.get('desde'):
            desde = parse_date(options['desde'])
            if desde:
                avisos = avisos.filter(creado_en__date__gte=desde)
        # Filtro por fecha final
        if options.get('hasta'):
            hasta = parse_date(options['hasta'])
            if hasta:
                avisos = avisos.filter(creado_en__date__lte=hasta)
        avisos = avisos.order_by('-creado_en')
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Mensaje', 'Nivel', 'Creado en', 'Visto', 'Usuario'])
            for aviso in avisos:
                writer.writerow([
                    aviso.id,
                    aviso.mensaje.replace('\n', ' '),
                    aviso.nivel,
                    aviso.creado_en.strftime('%Y-%m-%d %H:%M:%S'),
                    'Sí' if aviso.visto else 'No',
                    aviso.usuario.username if aviso.usuario else ''
                ])
        self.stdout.write(self.style.SUCCESS(f'Avisos exportados a {output_path}'))
