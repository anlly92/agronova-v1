from django.shortcuts import render, redirect,get_object_or_404
from .forms import IngresosEgresosform
from .models import IngresosEgresos
from django.db.models import Sum
from django.db.models.functions import ExtractDay
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from calendar import monthrange


def ingresos_egresos (request):
    if request.method == "POST":
        seleccion = request.POST.get("elemento")       # columna seleccionada
        accion = request.POST.get("accion")         # accion enviada "editar" o "borrar"

        if seleccion:

            if accion == "borrar":
                # elimina el elemento selecionado
                get_object_or_404(IngresosEgresos, pk=seleccion).delete()
                return redirect("ingresos_egresos")

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