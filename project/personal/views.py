from django.shortcuts import render,redirect
from .forms import Personalform
from .models import Empleado

def gestionar_personal (request):
    empleados = Empleado.objects.all()
    cantidad_filas_vacias = 15 - empleados.count()
    return render (request, 'personal/gestionar_personal.html', {'empleados': empleados, 'filas_vacias': range(cantidad_filas_vacias)})

def registro_personal (request):
    if request.method == 'POST':
        form = Personalform(request.POST)

        if form.is_valid():
            personal = form.save(commit=False) 
            personal.save()

            return redirect('gestionar_personal')
    else:
        form = Personalform()

    return render (request, 'personal/registrar_personal.html', {'form': form})

def actualizar_personal (request):
    return render (request, 'personal/actualizar_personal.html')

