from django.shortcuts import render

def procesos_agricolas (request):
    return render (request, 'procesos/mostrar_procesos_agricolas.html')

def registrar_procesos_agricolas (request):
    return render (request, 'procesos/registrar_proceso_agricola.html')

def proceso_de_produccion (request):
    return render (request, 'procesos/mostrar_proceso_produccion.html')

def registrar_proceso_de_produccion (request):
    return render (request, 'procesos/registrar_proceso_produccion.html')

