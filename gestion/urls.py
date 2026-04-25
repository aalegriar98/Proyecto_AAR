from django.urls import path
from . import views

urlpatterns = [
    # Login / Logout
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Inicio (dashboard)
    path('inicio/', views.inicio, name='inicio'),

    # Formularios
    path('registrar-herramienta/', views.registrar_herramienta, name='registrar_herramienta'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('registrar-prestamo/', views.registrar_prestamo, name='registrar_prestamo'),
    path('registrar-mantenimiento/', views.registrar_mantenimiento, name='registrar_mantenimiento'),
    path('editar-usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),

    # Listados
    path('herramientas/', views.listar_herramientas, name='listar_herramientas'),
    path('herramientas-disponibles/', views.herramientas_disponibles, name='herramientas_disponibles'),
    path('prestamos/', views.listar_prestamos, name='listar_prestamos'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('mantenimientos/', views.listar_mantenimientos, name='listar_mantenimientos'),

    # Acciones
    path('eliminar-prestamo/<int:id>/', views.eliminar_prestamo, name='eliminar_prestamo'),
    path('eliminar-mantenimiento/<int:id>/', views.eliminar_mantenimiento, name='eliminar_mantenimiento'),
    path('cambiar-estado-herramienta/<int:id>/', views.cambiar_estado_herramienta, name='cambiar_estado_herramienta'),
    path('alertas-atrasos/', views.alertas_atrasos, name='alertas_atrasos'),
]