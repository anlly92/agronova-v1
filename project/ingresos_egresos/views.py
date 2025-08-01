from django.shortcuts import render, redirect,get_object_or_404
from .forms import IngresosEgresosform,VentasForm
from .models import IngresosEgresos,Ventas
from administracion.models import Administrador
from inventarios.models import Inventario
from django.contrib.auth.models import User
from .forms import IngresosEgresosform
from .models import IngresosEgresos
from django.db.models import Sum
from django.db.models.functions import ExtractDay
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from calendar import monthrange
from django.db.models import Q
from decimal import InvalidOperation
from inventarios.utils import normalizar_texto, es_numero, parsear_fecha # funciones que se encunetran en utils en la app de inventarios

def ingresos_egresos(request):
    if request.method == "POST":
        seleccion = request.POST.get("elemento")
        accion = request.POST.get("accion")
        if seleccion:
            if accion == "borrar":
                get_object_or_404(IngresosEgresos, pk=seleccion).delete()
                return redirect("ingresos_egresos")

    buscar, Ingresos_Egresos, documento_admin, tipo, fecha, monto = filtrar_ingresos_egresos(request)
    cantidad_filas_vacias = 15 - Ingresos_Egresos.count()

    contexto = {
        'Ingresos_Egresos': Ingresos_Egresos,
        'filas_vacias': range(cantidad_filas_vacias),
        'buscar': buscar,
        'filtro_documento_admin': documento_admin,
        'filtro_tipo': tipo,
        'filtro_fecha': fecha,
        'filtro_monto': monto,
    }

    return render(request, 'ingresos_egresos/mostrar_ingresos_egresos.html', contexto)


def registro_ingresos_egresos (request):
    ok = False 
    if request.method == 'POST':
        form = IngresosEgresosform(request.POST)

        if form.is_valid():
            ingreso_egreso = form.save(commit=False) 
            ingreso_egreso.id_admin = Administrador.objects.get(correo=request.user.username)
            ingreso_egreso.save()

            ok = True 
    else:
        form = IngresosEgresosform()

    return render(request, 'ingresos_egresos/registro_ingresos_egresos.html', {'form': form,'ok':ok})


def filtrar_ingresos_egresos(request):
    documento_admin = request.GET.get("documento_admin", "")
    tipo = request.GET.get("tipo", "")
    fecha = request.GET.get("fecha", "")
    monto = request.GET.get("monto", "")
    buscar = request.GET.get("buscar", "").strip()

    Ingresos_Egresos = IngresosEgresos.objects.all()

    # Búsqueda general
    if buscar:
        buscar_normalizado = normalizar_texto(buscar)
        filtro_numerico = Q()
        filtro_texto = Q()
        filtro_fecha = Q()

        if es_numero(buscar_normalizado):
            try:
                filtro_numerico = (
                    Q(id_transaccion__iexact=buscar_normalizado) |
                    Q(id_admin__id_admin__iexact=buscar_normalizado) |
                    Q(monto=float(buscar_normalizado))
                )
            except (ValueError, InvalidOperation):
                filtro_numerico = Q()

        filtro_texto = (
            Q(tipo__iexact=buscar_normalizado) |
            Q(descripcion__icontains=buscar_normalizado) |
            Q(id_admin__nombre__iexact=buscar_normalizado)
        )

        fecha_parseada = parsear_fecha(buscar_normalizado)
        if fecha_parseada:
            filtro_fecha = Q(fecha=fecha_parseada)

        Ingresos_Egresos = Ingresos_Egresos.filter(
            filtro_numerico | filtro_texto | filtro_fecha
        )

    if documento_admin:
        try:
            documento_admin_int = int(documento_admin)
            Ingresos_Egresos = Ingresos_Egresos.filter(id_admin__id_admin=documento_admin_int)
        except ValueError:
            pass

    if tipo:
        Ingresos_Egresos = Ingresos_Egresos.filter(tipo__iexact=tipo)

    if fecha:
        Ingresos_Egresos = Ingresos_Egresos.filter(fecha=fecha)

    if monto:
        Ingresos_Egresos = Ingresos_Egresos.filter(monto=monto)

    return buscar, Ingresos_Egresos, documento_admin, tipo, fecha, monto


#-------------------------------------Informe anual----------------------------------------#
def informe_anual(request):
    # Si no hay 'anio', renderizar el HTML
    if 'anio' not in request.GET:
        return render(request, 'ingresos_egresos/informe_anual.html', {'now': datetime.now()})

    # Si hay 'anio', procesar la solicitud JSON
    anio = request.GET.get('anio')
    if not anio:
        return JsonResponse({'error': 'Parámetro "anio" no proporcionado.'}, status=400)

    try:
        anio = int(anio)
    except ValueError:
        return JsonResponse({'error': 'Parámetro "anio" inválido. Debe ser un número entero.'}, status=400)

    # Validar rango de años
    current_year = datetime.now().year
    if anio < 1900 or anio > current_year:
        return JsonResponse({'error': f'El año debe estar entre 1900 y {current_year}.'}, status=400)

    # Consulta para ingresos
    ingresos = IngresosEgresos.objects.filter(fecha__year=anio, tipo='Ingreso').annotate(
        mes=ExtractMonth('fecha')
    ).values('mes').annotate(
        total=Sum('monto')
    ).order_by('mes')

    # Consulta para egresos
    egresos = IngresosEgresos.objects.filter(fecha__year=anio, tipo='Egreso').annotate(
        mes=ExtractMonth('fecha')
    ).values('mes').annotate(
        total=Sum('monto')
    ).order_by('mes')

    montos_ingresos = [0.0] * 12
    montos_egresos = [0.0] * 12

    for item in ingresos:
        mes_index = item['mes'] - 1
        montos_ingresos[mes_index] = float(item['total'] or 0.0)

    for item in egresos:
        mes_index = item['mes'] - 1
        montos_egresos[mes_index] = float(item['total'] or 0.0)

    etiquetas = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", 
                "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

    # Mensaje opcional si no hay datos
    if not ingresos and not egresos:
        return JsonResponse({
            'labels': etiquetas,
            'data': {
                'ingresos': montos_ingresos,
                'egresos': montos_egresos
            },
            'warning': f'No se encontraron datos para el año {anio}.'
        })

    return JsonResponse({
        'labels': etiquetas,
        'data': {
            'ingresos': montos_ingresos,
            'egresos': montos_egresos
        }
    })

#----------------------------------Informe mensual -----------------------------------

def informe_mensual(request):
    return render(request, 'ingresos_egresos/informe_mensual.html')

# Vista para los datos del informe mensual
def datos_informe_mensual(request):
    # Obtener parámetros mes y anio
    mes_str = request.GET.get('mes')
    anio_str = request.GET.get('anio')
    
    # Validar que los parámetros estén presentes
    if not mes_str or not anio_str:
        return JsonResponse({'error': 'Parámetros requeridos'}, status=400)
    
    # Validar que los parámetros sean números
    try:
        mes = int(mes_str)
        anio = int(anio_str)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Valores inválidos'}, status=400)
    
    # Validar que el mes esté entre 1 y 12
    if mes < 1 or mes > 12:
        return JsonResponse({'error': 'Mes inválido'}, status=400)
    
    # Validar que el año esté en un rango razonable
    current_year = datetime.now().year
    if anio < 1900 or anio > current_year:
        return JsonResponse({'error': f'El año debe estar entre 1900 y {current_year}'}, status=400)
    
    # Obtener el número de días en el mes
    num_dias = monthrange(anio, mes)[1]
    
    # Obtener los datos de ingresos y egresos agrupados por día
    ingresos = IngresosEgresos.objects.filter(
        fecha__year=anio, fecha__month=mes, tipo='Ingreso'
    ).annotate(dia=ExtractDay('fecha')).values('dia').annotate(total=Sum('monto')).order_by('dia')
    
    egresos = IngresosEgresos.objects.filter(
        fecha__year=anio, fecha__month=mes, tipo='Egreso'
    ).annotate(dia=ExtractDay('fecha')).values('dia').annotate(total=Sum('monto')).order_by('dia')
    
    # Crear listas para los montos de ingresos y egresos
    montos_ingresos = [0.0] * num_dias
    montos_egresos = [0.0] * num_dias
    
    # Llenar las listas con los datos obtenidos
    for ingreso in ingresos:
        montos_ingresos[ingreso['dia'] - 1] = float(ingreso['total'])
    
    for egreso in egresos:
        montos_egresos[egreso['dia'] - 1] = float(egreso['total'])
    
    # Etiquetas para los días
    labels = [str(i) for i in range(1, num_dias + 1)]
    
    # Agregado manejo de datos vacíos con mensaje warning
    if not ingresos and not egresos:
        return JsonResponse({
            'warning': f'No se encontraron datos para el mes {mes}/{anio}',
            'labels': labels,
            'data': {'ingresos': montos_ingresos, 'egresos': montos_egresos}
        })
    
    # Retornar los datos en formato JSON
    return JsonResponse({
        'labels': labels,
        'data': {
            'ingresos': montos_ingresos,
            'egresos': montos_egresos
        }
    })

def informe_mensual (request):
    return render (request, 'ingresos_egresos/informe_mensual.html')

def ventas (request):
    if request.method == "POST":
        seleccion = request.POST.get("elemento")       # columna seleccionada
        accion = request.POST.get("accion")         # accion enviada "editar" o "borrar"

        if seleccion:

            if accion == "editar":
                # redirige al formulario de edición
                return redirect("actualizar_ventas", seleccion=seleccion)

            if accion == "borrar":
                # elimina el elemento selecionado
                get_object_or_404(Ventas,pk=seleccion).delete()
                return redirect("ventas")

    ventas = Ventas.objects.all()
    cantidad_filas_vacias = 15 - ventas.count()
    return render (request, 'ingresos_egresos/mostrar_ventas.html', {'ventas': ventas, 'filas_vacias': range(cantidad_filas_vacias)})

def registrar_ventas (request):
    ok = False 
    if request.method == 'POST':
        form = VentasForm(request.POST)

        if form.is_valid():
            
            venta = form.save(commit=False) 

            venta.id_admin = Administrador.objects.get(correo=request.user.username)
            
            producto = venta.id_producto
            precio_unitario = producto.precio_unitario
            total = venta.cantidad * precio_unitario

            if producto.stock >= venta.cantidad:
                producto.stock -= venta.cantidad
                producto.save()
                venta.save()

                # Registro automático en ingresos
                IngresosEgresos.objects.create(
                    id_admin=venta.id_admin,
                    tipo="Ingreso",
                    descripcion=f"Venta de {venta.cantidad} bolsas de {producto.nombre} de {producto.contenido} {producto.unidad} ",
                    fecha=venta.fecha,
                    monto=total
                )

                ok = True
            else:
                form.add_error('cantidad', 'No hay suficiente stock disponible.')
    else:
        form = VentasForm()

    productos = Inventario.objects.filter(tipo="Inventario Producto final")
    return render(request, 'ingresos_egresos/registrar_ventas.html', {'form': form,'productos': productos,'ok': ok})

def actualizar_ventas (request,seleccion):
    productos = Inventario.objects.filter(tipo="Inventario Producto final")
    return render (request, 'ingresos_egresos/actualizar_ventas.html',{'productos': productos})

def informe_ventas (request):
    return render (request, 'ingresos_egresos/informe_ventas.html')

