from django.urls import path
from personal import views

urlpatterns = [
    path("gestionar_personal/", views.gestionar_personal, name='gestionar_personal'),
    path("registro_del_personal/", views.registro_personal, name='registro_personal'),
    path('accion/', views.accion_personal, name='accion_personal'),
    path("<int:seleccion>/editar/", views.actualizar_personal, name='actualizar_personal'),

]