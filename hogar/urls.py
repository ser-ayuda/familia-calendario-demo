from django.contrib import admin
from django.urls import path, include
from tareas import views as tareas_views
from tareas.views_logout import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # Compatibility: accept POST/GET to /logout/ and delegate to the project's custom logout
    path('logout/', custom_logout, name='custom_logout'),
    path('demo/', tareas_views.demo_public, name='demo_public'),
    path('', include('tareas.urls')),
]
