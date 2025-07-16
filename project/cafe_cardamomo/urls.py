from django.urls import path
from cafe_cardamomo import views

urlpatterns = [
    path("gestionar_lote/", views.gestionar_lote, name='gestionar_lote'),
    path("registrar_lote/", views.registrar_lote, name='registrar_lote'),
    path("<int:seleccion>/editar/", views.actualizar_lote, name='actualizar_lote'),
    path("gestionar_recoleccion/", views.gestionar_recoleccion, name='gestionar_recoleccion'),
    path("registrar_recoleccion/", views.registrar_recoleccion, name='registrar_recoleccion'),
    path("registrar_pago/", views.registrar_pago, name='registrar_pago'),
    path("total_de_recoleccion/", views.total_de_recoleccion, name='total_de_recoleccion'),
]