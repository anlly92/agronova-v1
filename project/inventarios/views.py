from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProductoFinalform, Arbustosform, Agroquimicosform, Herramientasform
from .models import Inventario

# ────────── Producto final ──────────

def inventario_producto_final (request):
    if request.method == "POST":
        seleccion = request.POST.get("elemento")       # columna seleccionada
        accion = request.POST.get("accion")         # accion enviada "editar" o "borrar"

        if seleccion:

            if accion == "editar":
                # redirige al formulario de edición
                return redirect("actualizar_producto_final", seleccion=seleccion)

            if accion == "borrar":
                # elimina el elemento selecionado
                get_object_or_404(Inventario, pk=seleccion).delete()
                return redirect("inventario_producto_final")

    producto_final = Inventario.objects.filter(tipo='Inventario Producto final')
    cantidad_filas_vacias = 15 - producto_final.count()
    return render (request, 'inventarios/inventario_producto_final.html', {'producto_final': producto_final, 'filas_vacias': range(cantidad_filas_vacias)})

def registrar_inventario_producto_final (request):
    ok = False 
    if request.method == 'POST':
        form = ProductoFinalform(request.POST)

        if form.is_valid():
            ProductoFinal = form.save(commit=False) 
            ProductoFinal.tipo = 'Inventario Producto final'
            ProductoFinal.save()

            ok = True   
    else:
        form = ProductoFinalform()

    return render (request, 'inventarios/registrar_inventario_producto_final.html', {'form': form,'ok':ok})

def actualizar_producto_final (request,seleccion):
    return render (request, 'inventarios/actualizar_producto_final.html')

# ────────── Arbustos ──────────

def inventario_arbustos (request):
    if request.method == "POST":
        seleccion = request.POST.get("elemento")       # columna seleccionada
        accion = request.POST.get("accion")         # accion enviada "editar" o "borrar"

        if seleccion:

            if accion == "editar":
                # redirige al formulario de edición
                return redirect("actualizar_inventario_arbustos", seleccion=seleccion)

            if accion == "borrar":
                # elimina el elemento selecionado
                get_object_or_404(Inventario, pk=seleccion).delete()
                return redirect("inventario_arbustos")

    arbustos = Inventario.objects.filter(tipo='Inventario Arbustos')
    cantidad_filas_vacias = 15 - arbustos.count()
    return render (request, 'inventarios/inventario_arbustos.html',{'arbustos': arbustos, 'filas_vacias': range(cantidad_filas_vacias)})

def registrar_inventario_arbustos (request):
    ok = False 
    if request.method == 'POST':
        form = Arbustosform(request.POST)

        if form.is_valid():
            Arbusto = form.save(commit=False) 
            Arbusto.tipo = 'Inventario Arbustos'
            Arbusto.save()

            ok = True
    else:
        form = Arbustosform()

    return render (request, 'inventarios/registrar_inventario_arbustos.html', {'form': form,'ok':ok})

def actualizar_inventario_arbustos (request,seleccion):
    return render (request, 'inventarios/actualizar_arbustos.html')

# ────────── Agroquímicos ──────────

def inventario_agroquimicos (request):
    if request.method == "POST":
        seleccion = request.POST.get("elemento")       # columna seleccionada
        accion = request.POST.get("accion")         # accion enviada "editar" o "borrar"

        if seleccion:

            if accion == "editar":
                # redirige al formulario de edición
                return redirect("actualizar_inventario_agroquimicos", seleccion=seleccion)

            if accion == "borrar":
                # elimina el elemento selecionado
                get_object_or_404(Inventario, pk=seleccion).delete()
                return redirect("inventario_agroquimicos")

    agroquimicos = Inventario.objects.filter(tipo='Inventario Agroquimicos')
    cantidad_filas_vacias = 15 - agroquimicos.count()
    return render (request, 'inventarios/inventario_agroquimicos.html',{'agroquimicos': agroquimicos, 'filas_vacias': range(cantidad_filas_vacias)})

def registrar_inventario_agroquimicos (request):
    ok = False 
    if request.method == 'POST':
        form = Agroquimicosform(request.POST)

        if form.is_valid():
            Agroquimicos = form.save(commit=False) 
            Agroquimicos.tipo = 'Inventario Agroquimicos'
            Agroquimicos.save()

            ok = True   
    else:
        form = Agroquimicosform()

    return render (request, 'inventarios/registrar_inventario_agroquimicos.html', {'form': form,'ok':ok})

def actualizar_inventario_agroquimicos (request,seleccion):
    return render (request, 'inventarios/actualizar_agroquimico.html')

# ────────── Herramientas ──────────

def inventario_herramientas (request):
    if request.method == "POST":
        seleccion = request.POST.get("elemento")       # columna seleccionada
        accion = request.POST.get("accion")         # accion enviada "editar" o "borrar"

        if seleccion:

            if accion == "editar":
                # redirige al formulario de edición
                return redirect("actualizar_inventario_herramientas", seleccion=seleccion)

            if accion == "borrar":
                # elimina el elemento selecionado
                get_object_or_404(Inventario, pk=seleccion).delete()
                return redirect("inventario_herramientas")

    herramientas = Inventario.objects.filter(tipo='Inventario Herramientas')
    cantidad_filas_vacias = 15 - herramientas.count()
    return render (request, 'inventarios/inventario_herramientas.html',{'herramientas': herramientas, 'filas_vacias': range(cantidad_filas_vacias)})

def registrar_herramientas (request, categoria):
    ok = False 
    if request.method == 'POST':
        form = Herramientasform(request.POST)

        if form.is_valid():
            Herramientas = form.save(commit=False) 
            Herramientas.tipo = 'Inventario Herramientas'
            Herramientas.categoria = categoria
            Herramientas.save()

            ok = True   
    else:
        form = Herramientasform()

    return render (request, 'inventarios/registrar_herramienta_maquina.html', {'form': form, 'categoria': categoria,'ok':ok})

def actualizar_inventario_herramientas (request,seleccion):
    return render (request, 'inventarios/actualizar_herramienta_maquina.html')

def categoria_herramientas (request):
    return render (request, 'inventarios/categoria_herramienta_maquina.html')
