from django.shortcuts import render,redirect
from .forms import Agricolaform, Procesoform
from .models import Proceso


def procesos_agricolas (request):
    proceso_agricola = Proceso.objects.filter(tipo='Agrícola')
    cantidad_filas_vacias = 15 - proceso_agricola.count()
    return render (request, 'procesos/mostrar_procesos_agricolas.html', {'proceso_agricola': proceso_agricola, 'filas_vacias': range(cantidad_filas_vacias)})

def registrar_procesos_agricolas (request):
    if request.method == 'POST':
        form = Agricolaform(request.POST)

        if form.is_valid():
            Agricola = form.save(commit=False) 
            Agricola.tipo = 'Agrícola'
            Agricola.save()

            return redirect('procesos_agricolas')  
    else:
        form = Agricolaform()
    
    return render (request, 'procesos/registrar_proceso_agricola.html', {'form': form})

def proceso_de_produccion (request):
    proceso_produccion = Proceso.objects.filter(tipo='Producción')
    cantidad_filas_vacias = 15 - proceso_produccion.count()
    return render (request, 'procesos/mostrar_proceso_produccion.html', {'proceso_produccion': proceso_produccion, 'filas_vacias': range(cantidad_filas_vacias)})

def registrar_proceso_de_produccion (request):
    if request.method == 'POST':
        form = Procesoform(request.POST)

        if form.is_valid():
            Proceso = form.save(commit=False) 
            Proceso.tipo = 'Producción'
            Proceso.save()

            return redirect('proceso_de_produccion') 
        else:
            print("Errores del formulario:", form.errors)  # 👈 IMPORTANTE 
    else:
        form = Procesoform()
    
    return render (request, 'procesos/registrar_proceso_produccion.html', {'form': form})

