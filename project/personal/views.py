from django.shortcuts import render,redirect,get_object_or_404
from .forms import Personalform
from django.contrib import messages
from django.db import IntegrityError
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
    empleado = get_object_or_404(Empleado, pk=seleccion)

    if request.method == 'POST':
        telefono = request.POST.get("telefono","").strip()
        tipo_empleado = request.POST.get("tipo_empleado","").strip()
        pago_contrato = request.POST.get("pago_contrato","").strip()

        # Validación: al menos un campo debe estar lleno
        if not telefono and not tipo_empleado and not pago_contrato:
            messages.error(request, "Debes ingresar al menos un dato para actualizar.")
            return redirect("actualizar_personal", seleccion=seleccion)

        if telefono:
            empleado.telefono = telefono

        if tipo_empleado:
            empleado.tipo_empleado = tipo_empleado

        if pago_contrato:
            empleado.pago_contrato = pago_contrato

        empleado.save()
        return redirect("gestionar_personal")

    return render(request, 'personal/actualizar_personal.html', {'empleado': empleado})

