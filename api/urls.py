from django.urls import path
from . import views 

urlpatterns = [
    path('reportes/membresias/activas/', views.reporte_membresias_activas, name='reporte_membresias_activas'),
    path('reportes/membresias/por-tipo/', views.reporte_membresias_por_tipo, name='reporte_membresias_por_tipo'),
]