from django.shortcuts import render,redirect,get_object_or_404
from .forms import Personalform
from django.contrib import messages
from django.db import IntegrityError
from .models import Empleado
from inventarios.utils import normalizar_texto, es_numero # funciones que se encunetran en utils en la app de inventarios
from django.db.models import Q

def gestionar_personal(request):
    ok = False 
    # para acciones de editar y borrar
    if request.method == "POST":

        seleccion = request.POST.get("elemento")
        accion = request.POST.get("accion")

        if seleccion:
            if "," in seleccion:
                ids = seleccion.split(",")  
            else:
                ids = [seleccion]
        else:
            ids = []

        ids = [int(x) for x in ids if x.strip().isdigit()]

        if accion == "borrar" and ids:
            ok = True
            Empleado.objects.filter(pk__in=ids).delete()

        elif accion == "editar" and len(ids) == 1:
            ok = True
            return redirect("actualizar_personal", seleccion=ids[0])
            
    # llamamos y desempaquetamos los datos de la funcion filtrar empleados
    empleados, buscar, id_empleado, nombre, apellido, telefono, tipo_empleado, pago_contrato = filtrar_personal(request)
    # cantidad de filas vacías para mantener formato en tabla
    cantidad_filas_vacias = 15 - empleados.count()

    #contexto de los datos que se utilizan para filtrar o buscar en la barra
    contexto = {
        "empleados": empleados,
        "filas_vacias": range(cantidad_filas_vacias),
        "buscar": buscar,
        "filtro_id_empleado": id_empleado,
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "filtro_tipo_empleado": tipo_empleado,
        "filtro_pago_contrato": pago_contrato,
        "ok": ok,
    }

    return render(request, 'personal/gestionar_personal.html', contexto)



def registro_personal (request):
    ok = False 
    if request.method == 'POST':
        form = Personalform(request.POST)

        if form.is_valid():
            personal = form.save(commit=False) 
            personal.save()

            ok = True 
    else:
        form = Personalform()

    return render (request, 'personal/registrar_personal.html', {'form': form,'ok':ok})

def actualizar_personal (request,seleccion):
    ok = False
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
        ok = True

    return render(request, 'personal/actualizar_personal.html', {'empleado': empleado, 'ok': ok})

def filtrar_personal(request):
    
    buscar = request.GET.get("buscar", "").strip()
    id_empleado = request.GET.get("id_empleado", "")
    nombre = request.GET.get("nombre", "")
    apellido = request.GET.get("apellido", "")
    telefono = request.GET.get("telefono", "")
    tipo_empleado = request.GET.get("tipo_empleado", "")
    pago_contrato = request.GET.get("pago_contrato", "")

    
    empleados = Empleado.objects.all() 
    
    if buscar:
        buscar_normalizado = normalizar_texto(buscar)
        filtro_numerico = Q()
        filtro_texto = Q()
        if es_numero(buscar_normalizado):
            try:
                filtro_numerico = (
                    Q(id_empleado=int(buscar_normalizado)) |
                    Q(pago_contrato=float(buscar_normalizado))
                )
            except ValueError:
                pass


        partes = buscar_normalizado.split()

        for parte in partes:
            filtro_texto &= (
                Q(nombre__icontains=parte) |
                Q(apellido__icontains=parte) 
            )

        filtro_otros_datos = (
            Q(telefono__iexact=buscar_normalizado) |
            Q(tipo_empleado__iexact=buscar_normalizado) |
            filtro_numerico
        )


        empleados = Empleado.objects.filter(
            filtro_texto | filtro_numerico |filtro_otros_datos
        )

    # campos por los que se filtra en la modal
    if id_empleado:
        empleados = empleados.filter(id_empleado=id_empleado)

    if tipo_empleado:
        empleados = empleados.filter(tipo_empleado=tipo_empleado)

    if pago_contrato:
        try:
            pago_neto = float(pago_contrato.replace(".", "").replace(",", "."))
            empleados = empleados.filter(pago_contrato=pago_neto)
        except ValueError:
            pass

    return empleados, buscar, id_empleado, nombre, apellido, telefono, tipo_empleado, pago_contrato

