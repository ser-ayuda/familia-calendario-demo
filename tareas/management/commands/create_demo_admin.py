from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create or update a demo admin user (admin_demo/admin_demo)'

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        username = 'admin_demo'
        password = 'admin_demo'
        email = 'admin_demo@example.local'

        user, created = User.objects.get_or_create(username=username, defaults={
            'is_staff': True,
            'is_superuser': True,
            'email': email,
            'is_active': True,
        })
        if not created:
            user.is_staff = True
            user.is_superuser = True
            user.email = email
            user.is_active = True
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Admin ensured: {username} / {password}'))
