import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from tareas.models import AuditLog, Miembro, Evento


User = get_user_model()


def _anon_username(user, ts):
    return f"anon-{user.id}-{ts}"


def _anon_email(user):
    return f"anon-{user.id}@anonymized.example"


class Command(BaseCommand):
    help = 'Anonymize or delete data for users with deletion requests (uses AuditLog entries)'

    def add_arguments(self, parser):
        parser.add_argument('--ids', type=int, nargs='+', help='IDs of AuditLog (deletion_requested) to process')
        parser.add_argument('--all-completed', action='store_true', help='Process all deletion_requested entries that are not yet executed')
        parser.add_argument('--dry-run', action='store_true', help='Simulate actions without changing the database')
        parser.add_argument('--yes', action='store_true', help='Confirm actions without prompting')
        parser.add_argument('--delete-events', action='store_true', help='Delete events associated to the user instead of keeping history (default: keep history)')
        parser.add_argument('--output-json', type=str, help='Path to write a JSON report with actions performed')
        parser.add_argument('--admin-id', type=int, help='Admin user id to record as performer in AuditLog (optional)')

    def handle(self, *args, **options):
        ids = options.get('ids')
        all_completed = options.get('all_completed')
        dry_run = options.get('dry_run')
        delete_events = options.get('delete_events')
        confirm = options.get('yes')
        out_json = options.get('output_json')
        admin_id = options.get('admin_id')

        # Build queryset of AuditLog entries to process
        if ids:
            qs = AuditLog.objects.filter(id__in=ids, action='deletion_requested')
        elif all_completed:
            qs = AuditLog.objects.filter(action='deletion_requested')
        else:
            raise CommandError('Specify --ids or --all-completed')

        if not qs.exists():
            self.stdout.write('No deletion requests to process.')
            return

        to_report = []

        if not confirm and not dry_run:
            self.stdout.write(f'About to process {qs.count()} requests. Use --yes to skip confirmation or --dry-run to simulate.')
            ans = input('Continue? [y/N]: ').strip().lower()
            if ans != 'y':
                self.stdout.write('Aborted by user.')
                return

        for a in qs.order_by('created_at'):
            # Skip if already executed
            # SQLite backend may not support JSON contains lookup; check executed entries in Python
            executed = False
            for ex in AuditLog.objects.filter(action='deletion_executed'):
                d = ex.details or {}
                try:
                    if isinstance(d, dict) and d.get('completed_for') == a.id:
                        executed = True
                        break
                except Exception:
                    continue
            if executed:
                self.stdout.write(f'Entry id={a.id} already executed; skipping.')
                to_report.append({'id': a.id, 'status': 'skipped_already_executed'})
                continue

            # Determine user id
            target_user = None
            if a.user_id:
                try:
                    target_user = User.objects.get(id=a.user_id)
                except User.DoesNotExist:
                    target_user = None
            else:
                # try target_id field
                try:
                    if a.target_type.lower() == 'user' and a.target_id:
                        target_user = User.objects.filter(id=int(a.target_id)).first()
                except Exception:
                    target_user = None

            if target_user is None:
                self.stderr.write(f'Could not resolve user for AuditLog id={a.id}; marking failed.')
                AuditLog.objects.create(action='deletion_failed', user=None, target_type=a.target_type, target_id=a.target_id, details={'error': 'user_not_found', 'request_id': a.id})
                to_report.append({'id': a.id, 'status': 'failed', 'reason': 'user_not_found'})
                continue

            ts = timezone.now().strftime('%Y%m%d%H%M')
            summary = {'request_id': a.id, 'user_id': target_user.id, 'processed_at': ts, 'changes': {}}

            try:
                if dry_run:
                    # Compute what would happen
                    miembro_count = Miembro.objects.filter(usuario=target_user).count()
                    evento_count = Evento.objects.filter(miembro__usuario=target_user).count()
                    summary['changes'] = {'miembros': miembro_count, 'eventos': evento_count, 'user_change': 'would_anon'}
                    self.stdout.write(json.dumps(summary, ensure_ascii=False))
                    to_report.append({**summary, 'status': 'dry_run'})
                    continue

                # Real execution: wrap in atomic transaction
                with transaction.atomic():
                    # Anonymize user
                    old_username = target_user.username
                    target_user.username = _anon_username(target_user, ts)
                    target_user.email = _anon_email(target_user)
                    # clear name fields if present
                    if hasattr(target_user, 'first_name'):
                        target_user.first_name = ''
                    if hasattr(target_user, 'last_name'):
                        target_user.last_name = ''
                    target_user.set_unusable_password()
                    target_user.is_active = False
                    target_user.save()

                    # Miembros: anonymize and unlink
                    miembros = list(Miembro.objects.filter(usuario=target_user))
                    for m in miembros:
                        old_nombre = m.nombre
                        m.nombre = f'Anonimizado {m.id}'
                        m.usuario = None
                        m.save()

                    # Eventos: either delete or anonymize
                    if delete_events:
                        ev_count, _ = Evento.objects.filter(miembro__in=miembros).delete()
                        evento_count = ev_count
                    else:
                        # keep history but remove personal links
                        # Evento.miembro is non-nullable: create or reuse a placeholder Miembro and reassign eventos to it
                        placeholder_name = f'Anonimizado_user_{target_user.id}'
                        placeholder, created = Miembro.objects.get_or_create(nombre=placeholder_name, defaults={'usuario': None})
                        # Reassign eventos to placeholder (use miembro_id update) and clear creado_por
                        evento_qs = Evento.objects.filter(miembro__in=miembros)
                        evento_count = evento_qs.update(miembro_id=placeholder.id, creado_por=None)

                    # Record audit entry
                    AuditLog.objects.create(action='deletion_executed', user_id=admin_id if admin_id else None, target_type='user', target_id=str(target_user.id), details={'request_id': a.id, 'old_username': old_username, 'miembros_processed': [m.id for m in miembros], 'eventos_affected': evento_count})

                    summary['changes'] = {'old_username': old_username, 'miembros': [m.id for m in miembros], 'eventos_affected': evento_count}
                    to_report.append({**summary, 'status': 'completed'})
                    self.stdout.write(f'Processed request id={a.id} for user id={target_user.id} (miembros={len(miembros)}, eventos={evento_count})')

            except Exception as exc:
                self.stderr.write(f'Error processing request id={a.id}: {exc}')
                AuditLog.objects.create(action='deletion_failed', user_id=admin_id if admin_id else None, target_type='user', target_id=str(a.target_id or a.user_id), details={'error': str(exc), 'request_id': a.id})
                to_report.append({'id': a.id, 'status': 'failed', 'reason': str(exc)})

        # write report if requested
        if out_json:
            with open(out_json, 'w', encoding='utf-8') as fh:
                json.dump(to_report, fh, ensure_ascii=False, indent=2)
            self.stdout.write(f'Wrote report to {out_json}')

        self.stdout.write('Done.')
