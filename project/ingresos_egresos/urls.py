from django.urls import path
from ingresos_egresos import views
from .views import exportar_ingresos_egresos_excel, exportar_ingresos_egresos_pdf

urlpatterns = [
    path("ingresos_egresos/", views.ingresos_egresos, name='ingresos_egresos'),
    path("registro_ingresos_egresos/", views.registro_ingresos_egresos, name='registro_ingresos_egresos'),
    path("informe_anual/", views.informe_anual, name='informe_anual'),
    path("informe_mensual/", views.informe_mensual, name='informe_mensual'),
    path("datos_informe_mensual/", views.datos_informe_mensual, name='datos_informe_mensual'),  
    path('ingresos_egresos/exportar_excel/', exportar_ingresos_egresos_excel, name='exportar_ingresos_egresos_excel'),
    path('ingresos_egresos/exportar_pdf/', exportar_ingresos_egresos_pdf, name='exportar_ingresos_egresos_pdf'),

]

