from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum, F, Func, Value, Q # clase que sirve para construir consultas complejas
from django.db.models.functions import ExtractYear, ExtractMonth
from .forms import LoteForm, RecoleccionForm, PagosForm

from django.contrib import messages
from .models import Lote, Recoleccion, Empleado

from decimal import Decimal, InvalidOperation
from inventarios.utils import normalizar_texto, es_numero, parsear_fecha # funciones que se encunetran en utils en la app de inventarios

#Vistas para la gestion de los lotes 
def gestionar_lote(request):
    # para acciones de editar o borrar 
    if request.method == "POST":
        seleccion = request.POST.get("elemento")
        accion = request.POST.get("accion")

        if seleccion:
            if accion == "editar":
                return redirect("actualizar_lote", seleccion=seleccion)
            elif accion == "borrar":
                get_object_or_404(Lote, pk=seleccion).delete()
                return redirect("gestionar_lote")
            

    lotes, buscar, id_lote, nombre, hectareas, tipo_arbusto, estado = filtrar_lotes(request)
    cantidad_filas_vacias = lotes.count()

    contexto ={
        "Lotes": lotes,
        "filas_vacias": range(cantidad_filas_vacias),
        "buscar": buscar,
        "id_lote": id_lote,
        "nombre": nombre,
        "filtro_hectareas": hectareas,
        "filtro_tipo_arbusto": tipo_arbusto,
        "filtro_estado": estado,
    }
    return render(request, 'cafe_cardamomo/mostrar_lotes.html',contexto)


def registrar_lote (request):
    ok = False 
    if request.method == 'POST':
        form = LoteForm(request.POST)

        if form.is_valid():
            lote = form.save(commit=False) 
            lote.save()

            ok = True
    else:
        form = LoteForm()

    return render (request, 'cafe_cardamomo/registro_lote.html', {'form': form,'ok':ok})

def actualizar_lote (request,seleccion):
    lote = get_object_or_404(Lote, pk=seleccion)

    if request.method == 'POST':
        hectareas = request.POST.get("hectareas","").strip()
        tipo_arbusto = request.POST.get("tipo_arbusto","").strip()
        estado = request.POST.get("estado","").strip()

        # Validación: al menos un campo debe estar lleno
        if not hectareas and not tipo_arbusto and not estado:
            messages.error(request, "Debes ingresar al menos un dato para actualizar.")
            return redirect("actualizar_lote", seleccion=seleccion)

        if hectareas:
            lote.hectareas = hectareas

        if tipo_arbusto:
            lote.tipo_arbusto = tipo_arbusto

        if estado:
            lote.estado = estado
        lote.save()
        return redirect("gestionar_lote")

    return render(request, 'cafe_cardamomo/actualizar_lote.html', {'lote': lote})


#funcion para la barra de busqueda o filtro en lotes

def filtrar_lotes(request):
    buscar = request.GET.get("buscar", "").strip()
    id_lote = request.GET.get("id_lote", "").strip()
    nombre = request.GET.get("nombre", "").strip()#-----
    tipo_arbusto = request.GET.get("tipo_arbusto", "")
    estado = request.GET.get("estado", "")
    hectareas = request.GET.get("hectareas")

    lotes = Lote.objects.all()

    if buscar:
        buscar_normalizado = normalizar_texto(buscar)
        filtro_numerico = Q()
        filtro_texto = Q()
        if es_numero(buscar_normalizado):
            try:
                filtro_numerico = (
                    Q(id_lote=int(buscar_normalizado)) |
                    Q(hectareas=int(buscar_normalizado))
                )
            except ValueError:
                pass


        filtro_texto = (
            Q(nombre__iexact=buscar_normalizado)|
            Q(tipo_arbusto__iexact=buscar_normalizado)|
            Q(estado__iexact=buscar_normalizado)
        )

        lotes = Lote.objects.filter(
            filtro_numerico | filtro_texto
        )

    #campos utilizados en la modal del filtro
    if tipo_arbusto:
        lotes = lotes.filter(tipo_arbusto=tipo_arbusto)
    if estado:
        lotes = lotes.filter(estado=estado)
    if hectareas:
        lotes = lotes.filter(hectareas=hectareas)

    return lotes, buscar, id_lote, nombre, hectareas, tipo_arbusto, estado


def gestionar_recoleccion (request):
    lotes, recolecciones, empleados, buscar, id_empleado, id_lote, tipo_producto, kilos, horas, fecha, tipo_pago = filtrar_recoleccion(request)  
    cantidad_filas_vacias = recolecciones.count()

    contexto = {
        'recolecciones': recolecciones,
        'filas_vacias': range(cantidad_filas_vacias),
        'buscar': buscar,
        'lotes': lotes,
        'filtro_id_empleado': id_empleado,
        'filtro_id_lote': id_lote,
        'filtro_tipo_producto': tipo_producto,
        'filtro_kilos': kilos,
        'filtro_horas': horas,
        'filtro_fecha': fecha,
        'filtro_tipo_pago': tipo_pago,
        'empleados': empleados,
    }

    return render (request, 'cafe_cardamomo/mostrar_recoleccion.html',contexto)

def filtrar_recoleccion(request):
    buscar = request.GET.get("buscar", "").strip()
    id_empleado = request.GET.get("id_empleado", "")
    id_lote = request.GET.get("id_lote", "")
    tipo_producto = request.GET.get("tipo_producto", "")
    kilos = request.GET.get("kilos", "")
    horas = request.GET.get("horas_trabajadas", "")
    fecha = request.GET.get("fecha", "")
    tipo_pago = request.GET.get("tipo_pago", "")

    recolecciones = Recoleccion.objects.all()
    empleados = Empleado.objects.all()
    lotes = Lote.objects.all()

    if buscar:
        buscar_normalizado = normalizar_texto(buscar)
        filtro_numerico = Q()
        filtro_texto = Q()
        filtro_fecha = Q()

        # Filtra si es número exacto
        if es_numero(buscar_normalizado):
            try:
                filtro_numerico = (
                    Q(id_recoleccion=int(buscar_normalizado)) |
                    Q(id_empleado__id_empleado=int(buscar_normalizado)) |
                    Q(id_lote__id_lote=int(buscar_normalizado)) |
                    Q(kilos=int(buscar_normalizado)) |
                    Q(horas_trabajadas=Decimal(buscar_normalizado)) |
                    Q(tipo_pago__valor=int(buscar_normalizado))
                )
            except (ValueError, InvalidOperation):
                pass

        partes = buscar_normalizado.split()
        for parte in partes:
            filtro_texto &= (
            Q(id_empleado__nombre__icontains=parte) |
            Q(id_empleado__apellido__icontains=parte)
            )


        filtro_otros_datos = (
            Q(tipo_producto__iexact=buscar_normalizado) |
            Q(tipo_pago__tipo_pago__iexact=buscar_normalizado) |
            Q(id_lote__nombre__iexact=buscar_normalizado) 
        )
        # Filtro por fecha
        fecha_parseada = parsear_fecha(buscar)
        if fecha_parseada:
            filtro_fecha = Q(fecha=fecha_parseada)
        # Consulta combinada
        recolecciones = Recoleccion.objects.filter(
            filtro_numerico | filtro_texto | filtro_fecha | filtro_otros_datos
        )

    if id_empleado:
        try:
            id_empleado = int(id_empleado)
            recolecciones = recolecciones.filter(id_empleado=id_empleado)
        except ValueError:
            pass

    if id_lote:
        try:
            id_lote = int(id_lote)
            recolecciones = recolecciones.filter(id_lote=id_lote)
        except ValueError:
            pass

    if tipo_producto:
        recolecciones = recolecciones.filter(tipo_producto=tipo_producto)

    if kilos:
        try:
            kilos_decimal = Decimal(kilos)
            recolecciones = recolecciones.filter(kilos=kilos_decimal)
        except InvalidOperation:
            pass

    if horas:
        try:
            horas_decimal = Decimal(horas)
            recolecciones = recolecciones.filter(horas_trabajadas=horas_decimal)
        except InvalidOperation:
            pass

    if fecha:
        recolecciones = recolecciones.filter(fecha=fecha)

    if tipo_pago:
        recolecciones = recolecciones.filter(tipo_pago__tipo_pago=tipo_pago)

    return lotes, recolecciones, empleados, buscar, id_empleado, id_lote, tipo_producto, kilos, horas, fecha, tipo_pago  

def registrar_recoleccion (request):
    ok = False 
    if request.method == 'POST':
        form = RecoleccionForm(request.POST)

        if form.is_valid():
            recoleccion = form.save(commit=False) 
            recoleccion.save()
            
            ok = True
    else:
        form = RecoleccionForm()

    return render (request, 'cafe_cardamomo/registro_recoleccion.html', {'form': form,'ok':ok})

def registrar_pago (request):
    if request.method == 'POST':
        form = PagosForm(request.POST)

        if form.is_valid():
            pago = form.save(commit=False) 
            pago.save()

            return redirect('gestionar_recoleccion')
    else:
        form = PagosForm()

    return render (request, 'cafe_cardamomo/registrar_pago.html', {'form': form})

def total_de_recoleccion (request):
    consulta_total_recoleccion = (
        Recoleccion.objects
        .annotate(  # agrega campos adicionales calculados a cada fila antes de agrupar o contar
            año=ExtractYear('fecha'),
            mes=ExtractMonth('fecha'),
            nombre_lote=F('id_lote__nombre')
        )
        .values('año', 'mes', 'nombre_lote')
        .annotate(total_kilos=Sum('kilos'))
        .order_by('-año', '-mes')
    )

    cantidad_filas_vacias = 15 - consulta_total_recoleccion.count()
    return render (request, 'cafe_cardamomo/total_de_recoleccion.html', {'total_recoleccion': consulta_total_recoleccion,'filas_vacias': range(cantidad_filas_vacias)})