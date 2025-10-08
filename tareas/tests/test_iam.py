from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from tareas.models import Tarea, Reto, Miembro, Categoria

class IAMRolesPermisosTest(TestCase):
    def setUp(self):
        # Crear grupos y permisos si no existen
        from scripts.crear_roles_permisos import crear_roles
        crear_roles()
        self.admin_group = Group.objects.get(name='admin')
        self.miembro_group = Group.objects.get(name='miembro')
        self.admin_user = User.objects.create_user('admin1', password='adminpass')
        self.miembro_user = User.objects.create_user('miembro1', password='miembropass')
        self.admin_user.groups.add(self.admin_group)
        self.miembro_user.groups.add(self.miembro_group)

    def test_grupos_existen(self):
        self.assertTrue(Group.objects.filter(name='admin').exists())
        self.assertTrue(Group.objects.filter(name='miembro').exists())

    def test_permisos_admin(self):
        # Admin debe tener todos los permisos CRUD sobre los modelos
        modelos = [Tarea, Reto, Miembro, Categoria]
        for modelo in modelos:
            for codename in ['add', 'change', 'delete', 'view']:
                perm_codename = f'{codename}_{modelo.__name__.lower()}'
                perm = Permission.objects.get(codename=perm_codename)
                self.assertTrue(self.admin_user.has_perm(f'{perm.content_type.app_label}.{perm_codename}'))

    def test_permisos_miembro(self):
        # Miembro solo debe tener permiso de ver
        modelos = [Tarea, Reto, Miembro, Categoria]
        for modelo in modelos:
            view_codename = f'view_{modelo.__name__.lower()}'
            perm = Permission.objects.get(codename=view_codename)
            self.assertTrue(self.miembro_user.has_perm(f'{perm.content_type.app_label}.{view_codename}'))
            for codename in ['add', 'change', 'delete']:
                perm_codename = f'{codename}_{modelo.__name__.lower()}'
                perm = Permission.objects.get(codename=perm_codename)
                self.assertFalse(self.miembro_user.has_perm(f'{perm.content_type.app_label}.{perm_codename}'))
