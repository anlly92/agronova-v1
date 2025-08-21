from django.urls import path
from ingresos_egresos import views

from .views import exportar_ingresos_egresos_excel, exportar_ingresos_egresos_pdf, descargar_informe_mensual_excel, exportar_ventas_excel, exportar_ventas_pdf, exportar_ventas_grafico_excel

urlpatterns = [
    path("ingresos_egresos/", views.ingresos_egresos, name='ingresos_egresos'),
    path("registro_ingresos_egresos/", views.registro_ingresos_egresos, name='registro_ingresos_egresos'),
    path("informe_anual/", views.informe_anual, name='informe_anual'),
    path("informe_mensual/", views.informe_mensual, name='informe_mensual'),
    path("ventas/", views.ventas, name='ventas'),
    path("registrar_ventas/", views.registrar_ventas, name='registrar_ventas'),
    path('<int:seleccion>/editar/', views.actualizar_ventas,   name='actualizar_ventas'),
    path("informe_ventas/", views.informe_ventas, name='informe_ventas'),
    path("datos_informe_ventas/", views.datos_informe_ventas, name= 'datos_informe_ventas'),
    path("datos_informe_mensual/", views.datos_informe_mensual, name='datos_informe_mensual'),
    path('ingresos_egresos/exportar_excel/', exportar_ingresos_egresos_excel, name='exportar_ingresos_egresos_excel'),
    path('ingresos_egresos/exportar_pdf/', exportar_ingresos_egresos_pdf, name='exportar_ingresos_egresos_pdf'),
    path('descargar_informe_anual/', views.descargar_informe_anual, name='descargar_informe_anual'),
    path('descargar_informe_mensual_excel/', descargar_informe_mensual_excel, name='descargar_informe_mensual_excel'),
    path('ventas/exportar_excel/', exportar_ventas_excel, name='exportar_ventas_excel'),
    path('ventas/exportar_grafico_excel/', exportar_ventas_grafico_excel, name='exportar_ventas_grafico_excel'),
    path('ventas/exportar_pdf/', exportar_ventas_pdf, name='exportar_ventas_pdf'),

]
