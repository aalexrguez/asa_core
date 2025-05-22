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
]
