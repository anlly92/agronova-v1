from django.urls import path
from administracion import views

urlpatterns = [
    path("gestionar_administrador/", views.gestionar_administrador, name='gestionar_administrador'),
    path('accion/', views.accion_administrador, name='accion_administrador'),
    path('<int:seleccion>/editar/', views.actualizar_administrador,   name='editar_administrador'),
    path('<int:seleccion>/eliminar/', views.gestionar_administrador, name='eliminar_administrador'),
    path("registro_administrador/", views.registro_administrador, name='registro_administrador'),
    path("sobre_mi/", views.sobre_mi, name='sobre_mi'),
    path("editar_perfil/", views.editar_perfil, name='editar_perfil'),
]