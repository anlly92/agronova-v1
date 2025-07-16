from django.shortcuts import render,redirect,get_object_or_404
from .forms import Personalform
from .models import Empleado

def gestionar_personal (request):
    if request.method == "POST":
        seleccion = request.POST.get("elemento")       # columna seleccionada
        accion = request.POST.get("accion")         # accion enviada "editar" o "borrar"

        if seleccion:

            if accion == "editar":
                # redirige al formulario de edición
                return redirect("actualizar_personal", seleccion=seleccion)

            if accion == "borrar":
                # elimina el elemento selecionado
                get_object_or_404(Empleado, pk=seleccion).delete()
                return redirect("gestionar_personal")

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

def actualizar_personal (request,seleccion):
    return render (request, 'personal/actualizar_personal.html')

