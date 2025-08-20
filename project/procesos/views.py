from django.shortcuts import render,redirect
from .forms import Agricolaform, Procesoform
from .models import Proceso
from django.shortcuts import render, get_object_or_404, redirect
from personal.models import Empleado
from inventarios.models import Inventario
from cafe_cardamomo.models import Lote
from django.db.models import Q 
from decimal import InvalidOperation
from inventarios.utils import normalizar_texto, es_numero, parsear_fecha # funciones que se encunetran en utils en la app de inventarios


def procesos_agricolas(request):
    buscar, inventario, empleados, proceso_agricola, id_proceso, id_lote, nombre_lote, id_empleado, nombre, descripcion, id_inventario, cantidad, fecha = filtrar_procesos_agricolas(request)
    cantidad_filas_vacias = 15 - proceso_agricola.count()

    contexto = {
        "filas_vacias": range(cantidad_filas_vacias),
        "buscar": buscar,
        "inventario": inventario,
        "empleados": empleados,
        'proceso_agricola': proceso_agricola,

        # Filtros para mantener en formulario
        "filtro_id_proceso": id_proceso,
        "filtro_id_lote": id_lote,
        "filtro_nombre_lote": nombre_lote,
        "filtro_id_empleado": id_empleado,
        "filtro_nombre": nombre,
        "filtro_descripcion": descripcion,
        "filtro_id_inventario": id_inventario,
        "filtro_cantidad": cantidad,
        "filtro_fecha": fecha,
    }
    return render(request, 'procesos/mostrar_procesos_agricolas.html',contexto )


def registrar_procesos_agricolas (request):
    ok = False 

    if request.method == 'POST':
        form = Agricolaform(request.POST)

        if form.is_valid():
            proceso = form.save(commit=False)

            agroquimico = proceso.id_inventario
            empleado = proceso.id_empleado
            lote = proceso.id_lote

            if agroquimico:

                if agroquimico.stock is not None and proceso.cantidad is not None:

                    if proceso.cantidad > agroquimico.stock:
                        form.add_error('cantidad', 'La cantidad supera el stock disponible.')

                    else:
                        # Descontar del stock y guardar proceso
                        proceso.tipo = 'Agrícola'

                        proceso.nombre_agroquimico = agroquimico.nombre

                        if empleado:
                            proceso.nombre_empleado = empleado.nombre + " " + empleado.apellido

                        if lote:
                            proceso.nombre_lote = lote.nombre


                        proceso.save()

                        agroquimico.stock -= proceso.cantidad

                        agroquimico.save()

                        ok = True
                else:
                    form.add_error(None, 'Datos incompletos para realizar el descuento de stock.')
    else:
        form = Agricolaform()

    empleados = Empleado.objects.all()
    lotes = Lote.objects.all()
    agroquimicos = Inventario.objects.filter(tipo='Inventario Agroquimicos')
    return render(request, 'procesos/registrar_proceso_agricola.html', {'form': form,'ok': ok, 'empleados': empleados, 'lotes': lotes, 'agroquimicos': agroquimicos})

def filtrar_procesos_agricolas(request):
    buscar = request.GET.get("buscar", "").strip()
    id_proceso = request.GET.get("id_proceso", "")
    id_lote = request.GET.get("id_lote", "")
    nombre_lote = request.GET.get("nombre_lote", "")
    id_empleado = request.GET.get("id_empleado", "")
    nombre = request.GET.get("nombre", "")
    descripcion = request.GET.get("descripcion", "")
    id_inventario = request.GET.get("id_inventario", "")
    cantidad = request.GET.get("cantidad", "")
    fecha = request.GET.get("fecha", "")

    inventario = Inventario.objects.all()
    empleados = Empleado.objects.all()
    
    proceso_agricola = Proceso.objects.filter(tipo="Agrícola")

    if buscar:
        buscar_normalizado = normalizar_texto(buscar)
        filtro_numerico = Q()
        filtro_texto = Q()
        filtro_fecha = Q()
        filtro_otros_datos = Q()

        if es_numero(buscar_normalizado):
            try:
                filtro_numerico = (
                    Q(id_proceso=int(buscar_normalizado)) |
                    Q(id_empleado__id_empleado=int(buscar_normalizado)) |
                    Q(id_lote__id_lote=int(buscar_normalizado)) |
                    Q(id_inventario__id_inventario=int(buscar_normalizado)) |
                    Q(cantidad=int(buscar_normalizado))
                )
            except (ValueError, InvalidOperation):
                pass

        filtro_otros_datos = (
            Q(descripcion__icontains=buscar_normalizado) |
            Q(id_lote__nombre__icontains=buscar_normalizado) |
            Q(id_inventario__nombre__icontains=buscar_normalizado)
        )

        partes = buscar_normalizado.split()
        for parte in partes:
            filtro_texto &= (
                Q(id_empleado__nombre__icontains=parte) |
                Q(id_empleado__apellido__icontains=parte)
            )

        fecha_parseada = parsear_fecha(buscar)
        if fecha_parseada:
            filtro_fecha = Q(fecha=fecha_parseada)

        # Aplica todos los filtros a procesos agrícolas
        proceso_agricola = proceso_agricola.filter(
            filtro_numerico | filtro_texto | filtro_fecha | filtro_otros_datos
        )

    if id_lote:
        proceso_agricola = proceso_agricola.filter(id_lote__id_lote=id_lote)

    if nombre_lote:
        proceso_agricola = proceso_agricola.filter(id_lote__nombre__icontains=nombre_lote)

    if id_empleado:
        proceso_agricola = proceso_agricola.filter(id_empleado__id_empleado=id_empleado)
    
    if nombre:
        proceso_agricola = proceso_agricola.filter(id_inventario__nombre__icontains=nombre)
    
    if fecha:
        proceso_agricola = proceso_agricola.filter(fecha=fecha)
    
    return buscar, inventario, empleados, proceso_agricola, id_proceso, id_lote, nombre_lote, id_empleado, nombre, descripcion, id_inventario, cantidad, fecha


# vistas para gestionar procesos de producción
def proceso_de_produccion(request):
    
    empleados, procesos, buscar, id_proceso, id_empleado,nombre, apellido, tipo_producto, descripcion, cantidad, fecha = filtrar_proceso_de_produccion(request)
    # Filas vacías hasta completar 15
    cantidad_filas_vacias = 15 - procesos.count()

    contexto ={
        "proceso_produccion": procesos,
        "empleados": empleados,
        "filas_vacias": range(cantidad_filas_vacias),
        'buscar': buscar,
        # Filtros para mantener valores en el formulario
        "id_proceso":id_proceso,
        "filtro_id_empleado": id_empleado,
        "nombre": nombre,
        "apellido": apellido,
        "filtro_tipo_producto": tipo_producto,
        "filtro_descripcion": descripcion,
        "filtro_cantidad": cantidad,
        "filtro_fecha": fecha,
    }
    return render (request, 'procesos/mostrar_proceso_produccion.html',contexto)



def registrar_proceso_de_produccion (request):
    ok = False 
    if request.method == 'POST':
        form = Procesoform(request.POST)

        if form.is_valid():
            Proceso = form.save(commit=False) 

            empleado = Proceso.id_empleado
            Proceso.tipo = 'Producción'

            if empleado:
                Proceso.nombre_empleado = empleado.nombre + " " + empleado.apellido
            
            Proceso.save()

            ok = True  
        else:
            print("Errores del formulario:", form.errors)  # 👈 IMPORTANTE 
    else:
        form = Procesoform()

    empleados = Empleado.objects.all()
    return render (request, 'procesos/registrar_proceso_produccion.html', {'form': form,'ok':ok, 'empleados': empleados})


def filtrar_proceso_de_produccion(request):
    buscar = request.GET.get("buscar", "").strip()
    id_proceso = request.GET.get("id_proceso", "").strip()
    id_empleado = request.GET.get("id_empleado", "").strip()
    nombre = request.GET.get("nombre", "").strip()
    apellido = request.GET.get("apellido", "").strip()
    tipo_producto = request.GET.get("tipo_producto", "").strip()
    descripcion = request.GET.get("descripcion", "").strip()
    cantidad = request.GET.get("cantidad", "").strip()
    fecha = request.GET.get("fecha", "").strip()

    empleados = Empleado.objects.all()
    procesos = Proceso.objects.filter(tipo="Producción")

    if buscar:
        buscar_normalizado =  normalizar_texto(buscar)
        filtro_numerico = Q()
        filtro_texto = Q()
        filtro_fecha  = Q()

        #Se filtra si es un numero exacto
        if es_numero(buscar_normalizado):
            try:
                filtro_numerico  = (
                    Q(id_proceso=int(buscar_normalizado))|
                    Q(id_empleado__id_empleado=int(buscar_normalizado))|
                    Q(cantidad=int(buscar_normalizado))
                )
            except(ValueError, InvalidOperation):
                pass

        filtro_otros_datos = (
            Q(tipo_producto__iexact=buscar_normalizado)|
            Q(id_empleado__nombre__iexact=buscar_normalizado)|
            Q(descripcion__icontains=buscar_normalizado)
        )

        partes = buscar_normalizado.split()
        for parte in partes:
            filtro_texto &= (
                Q(id_empleado__nombre__icontains=parte) |
                Q(id_empleado__apellido__icontains=parte)
            )
        
        fecha_parseada = parsear_fecha(buscar)
        if fecha_parseada:
            filtro_fecha = Q(fecha=fecha_parseada)

        # Solo traer los procesos de tipo "Producción"
        procesos = Proceso.objects.filter(
            Q(tipo="Producción") & (filtro_numerico | filtro_texto | filtro_fecha | filtro_otros_datos)
        )

    # Solo traer los procesos de tipo "Producción"
    if id_empleado:
        procesos = procesos.filter(id_empleado__id_empleado=id_empleado)

    if tipo_producto:
        procesos = procesos.filter(tipo_producto=tipo_producto)

    if descripcion:
        procesos = procesos.filter(descripcion=descripcion)


    if cantidad:
        try:
            procesos = procesos.filter(cantidad=float(cantidad))
        except ValueError:
            pass

    if fecha:
        procesos = procesos.filter(fecha=fecha)
    
    return empleados, procesos, buscar, id_proceso, id_empleado,nombre, apellido, tipo_producto, descripcion, cantidad, fecha
