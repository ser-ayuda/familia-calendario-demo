from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings


def create_demo_user():
    from django.contrib.auth.models import User
    if not User.objects.filter(username='demo').exists():
        User.objects.create_user('demo', password='demo')

def create_admin_user():
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', email='', password='admin')

def reset_axes():
    try:
        from axes.models import AccessAttempt, AccessLog
        AccessAttempt.objects.all().delete()
        AccessLog.objects.all().delete()
    except Exception:
        pass

@receiver(post_migrate)
def post_migrate_actions(sender, **kwargs):
    if getattr(settings, 'CREATE_DEMO_USER', True):
        create_demo_user()
        create_admin_user()
    if getattr(settings, 'RESET_AXES', True):
        reset_axes()
