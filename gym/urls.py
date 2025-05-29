from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('usuario/',views.usuario,name='usuarios'),
    path('crearUsuario',views.crearUsuario,name='crearUsuario'),
    path('editar_usuario/<str:username>/', views.editar_usuario, name='editar_usuario'),
    path('membresias/',views.membresia,name='membresia'),
    path('crear_membresia/',views.crear_membresia,name='crear_membresia'),
    path('eliminar_usuario/<str:username>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('entrenadores/', views.lista_entrenadores, name='entrenadores'),
    path('crear_info_entrenador/<str:username>/', views.crear_info_entrenador, name='crear_info_entrenador'),
    path('asignar_entrenador/', views.asignar_entrenador, name='asignar_entrenador'),
    path('eliminar_asignacion/<str:cliente_username>/', views.eliminar_asignacion, name='eliminar_asignacion'),
    path('avances/', views.avances_fisicos_inicio, name='avances_fisicos_inicio'),
    path('registrar_avance/', views.registrar_avance_fisico, name='registrar_avance_fisico'),
    path('historial_avances/<str:username>/', views.historial_avances_cliente, name='historial_avances_cliente'),
    path('reportes/membresias_activas/', views.vista_reporte_membresias_activas, name='vista_reporte_membresias_activas'),
    path('reportes/membresias_por_tipo/', views.vista_reporte_membresias_por_tipo, name='vista_reporte_membresias_por_tipo'),
]
