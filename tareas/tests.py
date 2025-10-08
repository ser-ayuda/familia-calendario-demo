from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from tareas.models import Tarea, Aviso
from django.urls import reverse

class IAMTestCase(TestCase):
    def setUp(self):
        # Crear grupos
        self.admin_group, _ = Group.objects.get_or_create(name='admin')
        self.miembro_group, _ = Group.objects.get_or_create(name='miembro')
        # Crear usuarios
        self.admin = User.objects.create_user('admin', password='adminpass', is_staff=True)
        self.admin.groups.add(self.admin_group)
        self.miembro = User.objects.create_user('miembro', password='mipass')
        self.miembro.groups.add(self.miembro_group)
        # Crear tarea de ejemplo
        self.tarea = Tarea.objects.create(nombre='Test Tarea')
        self.client = Client()

    def test_admin_puede_crear_tarea(self):
        self.client.login(username='admin', password='adminpass')
        resp = self.client.post(reverse('tarea-list'), {'nombre': 'Nueva Tarea'})
        self.assertIn(resp.status_code, [200, 201, 302])

    def test_miembro_no_puede_crear_tarea(self):
        self.client.login(username='miembro', password='mipass')
        resp = self.client.post(reverse('tarea-list'), {'nombre': 'Otra Tarea'})
        self.assertIn(resp.status_code, [403, 302])

    def test_miembro_puede_ver_tarea(self):
        self.client.login(username='miembro', password='mipass')
        resp = self.client.get(reverse('tarea-list'))
        self.assertEqual(resp.status_code, 200)

    def test_admin_puede_borrar_tarea(self):
        self.client.login(username='admin', password='adminpass')
        resp = self.client.delete(reverse('tarea-detail', args=[self.tarea.id]))
        self.assertIn(resp.status_code, [200, 204, 302])

    def test_miembro_no_puede_borrar_tarea(self):
        self.client.login(username='miembro', password='mipass')
        resp = self.client.delete(reverse('tarea-detail', args=[self.tarea.id]))
        self.assertIn(resp.status_code, [403, 302])

    def test_auditoria_creacion_tarea(self):
        self.client.login(username='admin', password='adminpass')
        data = {
            'nombre': 'Tarea Auditada',
            'descripcion': 'desc',
            'icono': '',
            'tag': '',
            'puntuacion': 1,
            'premio': 0.10,
            'tiempo_estimado': 30,
            'recurrencia_tipo': 'none',
        }
        self.client.post(reverse('tarea-list'), data)
        avisos = Aviso.objects.all()
        print('Avisos generados:', [a.mensaje for a in avisos])
        self.assertTrue(Aviso.objects.filter(mensaje__icontains='crear').exists())

# Puedes añadir más tests para vistas web, expiración de sesión, etc.

