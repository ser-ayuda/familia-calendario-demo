from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from tareas.models import AuditLog


class Command(BaseCommand):
    help = 'List and mark as processed privacy requests (deletion_requested / export) in AuditLog'

    def add_arguments(self, parser):
        parser.add_argument('--list', action='store_true', help='List pending requests')
        parser.add_argument('--mark-completed', type=int, nargs='+', help='IDs of AuditLog entries to mark as completed')

    def handle(self, *args, **options):
        if options['list']:
            qs = AuditLog.objects.filter(action__in=['deletion_requested', 'export']).order_by('created_at')
            if not qs.exists():
                self.stdout.write('No pending requests found.')
                return
            self.stdout.write('Pending requests:')
            for a in qs:
                self.stdout.write(f"ID {a.id} | action={a.action} | user_id={a.user_id} | target={a.target_type}:{a.target_id} | created={a.created_at:%Y-%m-%d %H:%M} | details={a.details}")
            return

        ids = options.get('mark_completed')
        if ids:
            for entry_id in ids:
                try:
                    a = AuditLog.objects.get(id=entry_id)
                except AuditLog.DoesNotExist:
                    self.stderr.write(f'Entry id={entry_id} not found')
                    continue
                # create a follow-up audit entry to record completion
                AuditLog.objects.create(
                    action='deletion_executed' if a.action == 'deletion_requested' else 'export',
                    user=None,
                    target_type=a.target_type,
                    target_id=a.target_id,
                    details={'completed_for': a.id, 'original_details': a.details, 'processed_at': timezone.now().isoformat()},
                )
                self.stdout.write(f'Marked entry id={entry_id} as completed (audit recorded).')
            return

        raise CommandError('Specify --list or --mark-completed <ids>')
