from django.urls import path
from core import views

urlpatterns = [
    path("", views.mostrar_home, name="home"),
    path("login/", views.mostrar_login, name="login"),
    path("inicio/", views.mostrar_inicio, name="inicio"),
    path("que_es_agronova/", views.que_es_agronova, name="que_es_agronova"),
    path("como_surgio_agronova/", views.como_surgio, name='como_surgio_agronova'),
    path("ventajas/", views.ventajas, name='ventajas'),
    path("mision_y_vision_agronova/", views.mision_y_vision_agronova, name='mision_y_vision_agronova'),
    path("historia/", views.historia, name='historia'),
    path("mision_y_vision_de_la_elisa/", views.mision_y_vision_elisa, name='mision_y_vision_la_elisa'),
    path("contraseña/", views.contraseña, name='contraseña'),
    path("terminos_condiciones/", views.terminos_condiciones, name='terminos_condiciones'),
]