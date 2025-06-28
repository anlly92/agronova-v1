from django.shortcuts import render

def ingresos_egresos (request):
    return render (request, 'ingresos_egresos/mostrar_ingresos_egresos.html')

def registro_ingresos_egresos (request):
    return render (request, 'ingresos_egresos/registro_ingresos_egresos.html')

def informe_anual (request):
    return render (request, 'ingresos_egresos/informe_anual.html')

def informe_mensual (request):
    return render (request, 'ingresos_egresos/informe_mensual.html')