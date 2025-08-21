from django.urls import path
from administracion import views

urlpatterns = [
    path("gestionar_administrador/", views.gestionar_administrador, name='gestionar_administrador'),
    path("registro_administrador/", views.registro_administrador, name='registro_administrador'),
    path("sobre_mi/", views.sobre_mi, name='sobre_mi'),
    path("editar_perfil/", views.editar_perfil, name='editar_perfil'),
]
