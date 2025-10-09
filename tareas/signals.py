from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings


def create_demo_user():
    from django.contrib.auth.models import User
    if not User.objects.filter(username='demo').exists():
        User.objects.create_user('demo', password='demo')

def create_admin_user():
    # Intentionally left empty to avoid creating an admin user with a
    # hard-coded password. Admin accounts must be created manually by the
    # maintainer via a secure channel.
    return

def reset_axes():
    try:
        from axes.models import AccessAttempt, AccessLog
        AccessAttempt.objects.all().delete()
        AccessLog.objects.all().delete()
    except Exception:
        pass

@receiver(post_migrate)
def post_migrate_actions(sender, **kwargs):
    # Only create demo user if explicitly enabled (avoid auto-creating
    # accounts on production deploys). Set environment variable
    # DJANGO_CREATE_DEMO_USER=True to enable during development.
    if getattr(settings, 'CREATE_DEMO_USER', False):
        create_demo_user()
    if getattr(settings, 'RESET_AXES', True):
        reset_axes()
