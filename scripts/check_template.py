import os
import sys
# ensure project root is on sys.path so 'hogar' package can be imported
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hogar.settings')
import django
django.setup()
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.conf import settings
try:
    t = get_template('registration/login.html')
    print('TEMPLATE_OK', t)
except TemplateDoesNotExist as e:
    print('TEMPLATE_MISSING', e)
    print('TEMPLATE_DIRS:', settings.TEMPLATES[0].get('DIRS'))
    print('APP_DIRS:', settings.TEMPLATES[0].get('APP_DIRS'))
    import pkgutil
    print('tareas package exists?', pkgutil.find_loader('tareas') is not None)
