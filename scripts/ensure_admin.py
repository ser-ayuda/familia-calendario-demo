"""Ensure a local admin user exists for capturing admin screenshots.

Creates or updates a superuser with username `admin_demo` and password `admin_demo`.
Run with the project's Python: .venv\Scripts\python.exe scripts\ensure_admin.py
"""
import os
from django.core.exceptions import ImproperlyConfigured

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hogar.settings')

try:
    import django
    django.setup()
except Exception as e:
    raise

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

print(f"Admin ensured: {username} / {password}")
