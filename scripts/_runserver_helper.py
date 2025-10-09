import os
import sys
from django.core.management import execute_from_command_line

repo_root = r"C:\Users\j\familia_calendario_public"
os.chdir(repo_root)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
# Ensure settings module for this helper
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hogar.settings')

execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
