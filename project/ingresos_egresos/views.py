from django.shortcuts import render, redirect
from .forms import IngresosEgresosform
from .models import IngresosEgresos

def ingresos_egresos (request):
    Ingresos_Egresos = IngresosEgresos.objects.all()
    cantidad_filas_vacias = 15 - Ingresos_Egresos.count()
    return render (request, 'ingresos_egresos/mostrar_ingresos_egresos.html', {'Ingresos_Egresos': Ingresos_Egresos, 'filas_vacias': range(cantidad_filas_vacias)})

def registro_ingresos_egresos (request):
    if request.method == 'POST':
        form = IngresosEgresosform(request.POST)

        if form.is_valid():
            ingreso_egreso = form.save(commit=False) 
            ingreso_egreso.save()


            return redirect('ingresos_egresos')  
    else:
        form = IngresosEgresosform()

    return render(request, 'ingresos_egresos/registro_ingresos_egresos.html', {'form': form})

def informe_anual (request):
    return render (request, 'ingresos_egresos/informe_anual.html')

def informe_mensual (request):
    return render (request, 'ingresos_egresos/informe_mensual.html')