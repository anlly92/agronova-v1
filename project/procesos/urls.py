from django.urls import path
from procesos import views

urlpatterns = [
    path("procesos_agricolas/", views.procesos_agricolas, name='procesos_agricolas'),
    path("registrar_procesos_agricolas/", views.registrar_procesos_agricolas, name='registrar_procesos_agricolas'),
    path("proceso_de_produccion/", views.proceso_de_produccion, name='proceso_de_produccion'),
    path("registrar_proceso_de_produccion/", views.registrar_proceso_de_produccion, name='registrar_proceso_de_produccion'),
]