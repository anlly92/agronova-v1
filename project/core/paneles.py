import io, base64, locale
from calendar import month_abbr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from cafe_cardamomo.models import Recoleccion, Lote
from ingresos_egresos.models import Ventas, IngresosEgresos
from inventarios.models import Inventario
from procesos.models import Proceso
from personal.models import Empleado
from core.quickstart import listar_eventos

def produccion_mensual ():
    hoy = timezone.now()
    mes_actual = hoy.month
    año_actual = hoy.year

    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain')
    except locale.Error:
        locale.setlocale(locale.LC_TIME, '') # fallback si falla

    # Consulta agrupada por tipo_producto para el mes y año actual
    produccion_mes = (
        Recoleccion.objects
        .filter(fecha__month=mes_actual, fecha__year=año_actual)
        .values('tipo_producto')
        .annotate(total_kilos=Sum('kilos'))
    )

    # Convertimos a diccionario
    produccion = {'Café': 0,'Cardamomo': 0}

    for item in produccion_mes:
        tipo = item['tipo_producto']
        kilos = item['total_kilos'] or 0
        produccion[tipo] = kilos

    nombre_mes = hoy.strftime('%B').capitalize()
    return produccion, nombre_mes

def agroquimicos_mas_usados():
    hoy = timezone.now()
    mes_actual = hoy.month
    año_actual = hoy.year

    # Filtrar procesos agrícolas con inventario asignado
    agroquimicos_mes = (
        Proceso.objects
        .filter(tipo='Agrícola', fecha__year=año_actual, fecha__month=mes_actual, id_inventario__isnull=False)
        .values('id_inventario__nombre','id_inventario__stock','id_inventario__unidad')
        .annotate(total_usado=Sum('cantidad'))
        .order_by('-total_usado')[:2]
    )

    nombre_mes = hoy.strftime('%B').capitalize()
    return agroquimicos_mes,nombre_mes

def producto_mas_vendido():
    hoy = timezone.now()
    mes_actual = hoy.month
    año_actual = hoy.year

    producto= (
        Ventas.objects
        .filter(fecha__year=año_actual, fecha__month=mes_actual)
        .values('id_producto__nombre','id_producto__contenido','id_producto__unidad')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')[:2]
    )

    nombre_mes = hoy.strftime('%B').capitalize()
    return producto,nombre_mes

def finanzas_del_mes():
    hoy = timezone.now()
    mes_actual = hoy.month
    año_actual = hoy.year

    datos = (
        IngresosEgresos.objects
        .filter(fecha__year=año_actual, fecha__month=mes_actual)
        .values('tipo')
        .annotate(total=Sum('monto'))
    )

    finanzas = {'Ingreso': 0, 'Egreso': 0}

    for item in datos:
        tipo = item['tipo']
        monto = item['total'] or 0
        finanzas[tipo] = monto

    nombre_mes = hoy.strftime('%B').capitalize()
    return finanzas, nombre_mes

def obtener_alertas():
    alertas = []
    hoy = timezone.now()
    mes_actual = hoy.month
    año_actual = hoy.year

    # 1. Productos con poco stock (< 10)
    pocos_stock = Inventario.objects.filter(tipo='Inventario Producto final', stock__lt=10)
    for producto in pocos_stock:
        alertas.append(f"⚠  Poco stock de {producto.nombre} {producto.contenido} {producto.unidad}: {round(producto.stock)} unidades")

    # 2. Herramientas en mal estado
    malas = Inventario.objects.filter(tipo='Inventario Herramientas', estado='Mala')
    for herramienta in malas:
        alertas.append(f"🛠  Herramienta en mal estado: {round(herramienta.stock)} {herramienta.nombre}")

    # 3. Bajón de producción respecto al mes anterior (30%)
    produccion_actual, _ = produccion_mensual()
    total_actual = sum(produccion_actual.values())

    mes_pasado = hoy - timezone.timedelta(days=30)
    produccion_pasada = (
        Recoleccion.objects
        .filter(fecha__year=mes_pasado.year, fecha__month=mes_pasado.month)
        .aggregate(total=Sum('kilos'))['total'] or 0
    )

    if produccion_pasada > 0:
        diferencia = produccion_pasada - total_actual
        porcentaje = (diferencia / produccion_pasada) * 100
        if porcentaje >= 30:
            alertas.append(f"📉 La producción bajó un {int(porcentaje)}% respecto al mes anterior.")
    
    # 4.  Agroquímicos con poco stock (< 5)
    pocos_stock_agroquimicos = Inventario.objects.filter(tipo='Inventario Agroquimicos', stock__lt=5)
    for agro in pocos_stock_agroquimicos:
        alertas.append(f"⚠  Poco stock de {agro.nombre} {agro.contenido} {agro.unidad}: {round(agro.stock)} unidades")
    
    # 5. Egresos mayores que ingresos
    finanzas, _ = finanzas_del_mes()
    if finanzas['Egreso'] > finanzas['Ingreso']:
        alertas.append(f"📉 Egresos mayores que ingresos de este mes: ${int(finanzas['Egreso'])} vs ${int(finanzas['Ingreso'])}")

    # 6. Arbustos de café sin renovar (más de 7 años y sin marcar renovación)
    hace_siete = hoy.replace(year=hoy.year - 7)
    arbustos_sin_renovar = Inventario.objects.filter(tipo_arbusto='Café', fecha_siembra__lt=hace_siete)
    for arbusto in arbustos_sin_renovar:

        
        if arbusto.id_lote is not None:
            alertas.append(f"📅 {round(arbusto.stock)} Arbustos de café sin renovar desde {arbusto.fecha_siembra.strftime('%d/%m/%Y')}: {arbusto.nombre} en el {arbusto.id_lote.nombre}")
        else:
            continue

    return alertas

def cantidad_de_empleados():
    vinculados = Empleado.objects.filter(tipo_empleado='Vinculado').count()
    no_vinculados = Empleado.objects.filter(tipo_empleado='No vinculado').count()
    total = vinculados + no_vinculados
    
    return {'vinculados': vinculados,'no_vinculados': no_vinculados,'total': total}

def recoleccion_mensual_grafico():
    hoy = timezone.now()
    año_actual = hoy.year

    datos = (
        Recoleccion.objects
        .filter(fecha__year=año_actual)
        .annotate(mes=TruncMonth('fecha'))
        .values('mes', 'tipo_producto')
        .annotate(total=Sum('kilos'))
    )

    meses_orden = [month_abbr[i] for i in range(1, 13)]
    meses = sorted(set([d['mes'].strftime('%b') for d in datos]), key=lambda m: meses_orden.index(m))
    cafe_dict = {d['mes'].strftime('%b'): d['total'] for d in datos if d['tipo_producto'] == 'Café'}
    carda_dict = {d['mes'].strftime('%b'): d['total'] for d in datos if d['tipo_producto'] == 'Cardamomo'}

    cafe = [cafe_dict.get(mes, 0) for mes in meses] 
    cardamomo = [carda_dict.get(mes, 0) for mes in meses] 

    # Gráfico separado
    x = np.arange(len(meses))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(x - width/2, cafe, width, label='Café', color='#780301')
    ax.bar(x + width/2, cardamomo, width, label='Cardamomo', color='#4b7510')

    ax.set_xticks(x)
    ax.set_xticklabels(meses)
    legend = ax.legend(facecolor='none', edgecolor='none', labelcolor='white')

    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(colors='white')

    # Quitar fondo
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    buffer = io.BytesIO()
    plt.tight_layout()

    plt.savefig(buffer, format='png', transparent=True)  # <- importante
    plt.close(fig)
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return imagen_base64

def calendario_de_tareas():
    eventos = listar_eventos(10)
    resumen = []
    for e in eventos:
        resumen.append({
            "title": e.get("summary", "Sin título"),
            "start": e["start"].get("dateTime", e["start"].get("date")),
            "end": e["end"].get("dateTime", e["end"].get("date")),
            "extendedProps": {
                "google_event_id": e["id"],
            }
        })
    return resumen
