from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum, F, Func, Value
from django.db.models.functions import ExtractYear, ExtractMonth
from .forms import LoteForm, RecoleccionForm, PagosForm
from .models import Lote, Recoleccion

def gestionar_lote (request):
    if request.method == "POST":
        seleccion = request.POST.get("elemento")       # columna seleccionada
        accion = request.POST.get("accion")         # accion enviada "editar" o "borrar"

        if seleccion:

            if accion == "editar":
                # redirige al formulario de edición
                return redirect("actualizar_lote", seleccion=seleccion)

            if accion == "borrar":
                # elimina el elemento selecionado
                get_object_or_404(Lote, pk=seleccion).delete()
                return redirect("gestionar_lote")

    Lotes = Lote.objects.all()
    cantidad_filas_vacias = 15 - Lotes.count()
    return render (request, 'cafe_cardamomo/mostrar_lotes.html', {'Lotes': Lotes, 'filas_vacias': range(cantidad_filas_vacias)})

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
    return render (request, 'cafe_cardamomo/actualizar_lote.html')

def gestionar_recoleccion (request):
    recolecciones = Recoleccion.objects.all()
    cantidad_filas_vacias = 15 - recolecciones.count()
    return render (request, 'cafe_cardamomo/mostrar_recoleccion.html', {'recolecciones': recolecciones, 'filas_vacias': range(cantidad_filas_vacias)})

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