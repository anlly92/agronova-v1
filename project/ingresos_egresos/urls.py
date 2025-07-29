from django.urls import path
from ingresos_egresos import views

urlpatterns = [
    path("ingresos_egresos/", views.ingresos_egresos, name='ingresos_egresos'),
    path("registro_ingresos_egresos/", views.registro_ingresos_egresos, name='registro_ingresos_egresos'),
    path("informe_anual/", views.informe_anual, name='informe_anual'),
    path("informe_mensual/", views.informe_mensual, name='informe_mensual'),
    path("datos_informe_mensual/", views.datos_informe_mensual, name='datos_informe_mensual'),  # Nueva ruta
]