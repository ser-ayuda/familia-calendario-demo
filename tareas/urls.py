from tareas.views import borrar_eventos_futuros
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    home, calendario, admin_tareas, lista_tareas, admin_eventos,
    MiembroViewSet, TareaViewSet, CategoriaViewSet, EventoViewSet,
# RETO_REMOVED:     retos_lista, proponer_reto, admin_retos, aprobar_reto, rechazar_reto,
    marcar_aviso_visto
)
from tareas import views
from tareas.views import politica_privacidad


router = DefaultRouter()
router.register(r'miembros', MiembroViewSet, basename='miembro')
router.register(r'tareas', TareaViewSet, basename='tarea')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'eventos', EventoViewSet, basename='evento')


urlpatterns = [
    path('', home, name='home'),
    path('calendario/', calendario, name='calendario'),
    path('tareas/', lista_tareas, name='lista_tareas'),
    path('gestion/', admin_tareas, name='admin_tareas'),
    path('eventos/', admin_eventos, name='admin_eventos'),
    path('miembros/', views.admin_miembros, name='admin_miembros'),
# RETO_REMOVED:     path('retos/', admin_retos, name='admin_retos'),
# RETO_REMOVED:     path('retos/aprobar/<int:reto_id>/', aprobar_reto, name='aprobar_reto'),
# RETO_REMOVED:     path('retos/rechazar/<int:reto_id>/', rechazar_reto, name='rechazar_reto'),
# RETO_REMOVED:     path('retos-publicos/', retos_lista, name='retos_lista'),
# RETO_REMOVED:     path('proponer-reto/', proponer_reto, name='proponer_reto'),
    path('api/', include(router.urls)),
    re_path(r'^api/eventos/(?P<pk>\d+)/marcar/$', views.EventoViewSet.as_view({'post': 'marcar'}), name='evento-marcar'),
    re_path(r'^api/eventos/(?P<pk>\d+)/aprobar/$', views.EventoViewSet.as_view({'post': 'aprobar'}), name='evento-aprobar'),
    path('avisos/marcar_visto/<int:aviso_id>/', marcar_aviso_visto, name='marcar_aviso_visto'),
    path('api/tareas/<int:tarea_id>/borrar_eventos_futuros/', views.borrar_eventos_futuros, name='borrar_eventos_futuros'),
    path('privacidad/', politica_privacidad, name='politica_privacidad'),
    path('privacy/request-export/', views.request_data_export, name='request_data_export'),
    path('privacy/request-deletion/', views.request_account_deletion, name='request_account_deletion'),
]

