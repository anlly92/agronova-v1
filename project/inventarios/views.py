from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProductoFinalform, Arbustosform, Agroquimicosform, Herramientasform
from .models import Inventario
from django.contrib import messages

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
    if request.method == 'POST':
        form = ProductoFinalform(request.POST)

        if form.is_valid():
            ProductoFinal = form.save(commit=False) 
            ProductoFinal.tipo = 'Inventario Producto final'
            ProductoFinal.save()

            return redirect('inventario_producto_final')  
    else:
        form = ProductoFinalform()

    return render (request, 'inventarios/registrar_inventario_producto_final.html', {'form': form})

def actualizar_producto_final (request,seleccion):
    inventario = get_object_or_404(Inventario, pk=seleccion)

    if request.method == 'POST':
        nombre = request.POST.get("nombre","").strip()
        precio_unitario = request.POST.get("precio_unitario","").strip()
        stock = request.POST.get("stock","").strip()

        # Validación: al menos un campo debe estar lleno
        if not nombre and not precio_unitario and not stock:
            messages.error(request, "Debes ingresar al menos un dato para actualizar.")
            return redirect("actualizar_producto_final", seleccion=seleccion)

        if nombre:
            inventario.nombre = nombre

        if precio_unitario:
            inventario.precio_unitario = precio_unitario

        if stock:
            inventario.stock = stock

        inventario.save()
        return redirect("inventario_producto_final")

    return render(request, 'inventarios/actualizar_producto_final.html', {'inventario': inventario})


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
    if request.method == 'POST':
        form = Arbustosform(request.POST)

        if form.is_valid():
            Arbusto = form.save(commit=False) 
            Arbusto.tipo = 'Inventario Arbustos'
            Arbusto.save()

            return redirect('inventario_arbustos')  
    else:
        form = Arbustosform()

    return render (request, 'inventarios/registrar_inventario_arbustos.html', {'form': form})

def actualizar_inventario_arbustos (request,seleccion):
    inventario = get_object_or_404(Inventario, pk=seleccion)

    if request.method == 'POST':
        stock = request.POST.get("stock","").strip()
        fecha_siembra = request.POST.get("fecha_siembra","").strip()

        # Validación: al menos un campo debe estar lleno
        if not stock and not fecha_siembra:
            messages.error(request, "Debes ingresar al menos un dato para actualizar.")
            return redirect("actualizar_inventario_arbustos", seleccion=seleccion)

        if stock:
            inventario.stock = stock

        if fecha_siembra:
            inventario.fecha_siembra = fecha_siembra

        inventario.save()
        return redirect("inventario_arbustos")

    return render(request, 'inventarios/actualizar_arbustos.html', {'inventario': inventario})

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
    if request.method == 'POST':
        form = Agroquimicosform(request.POST)

        if form.is_valid():
            Agroquimicos = form.save(commit=False) 
            Agroquimicos.tipo = 'Inventario Agroquimicos'
            Agroquimicos.save()

            return redirect('inventario_agroquimicos')  
    else:
        form = Agroquimicosform()

    return render (request, 'inventarios/registrar_inventario_agroquimicos.html', {'form': form})

def actualizar_inventario_agroquimicos (request,seleccion):
    inventario = get_object_or_404(Inventario, pk=seleccion)

    if request.method == 'POST':
        descripcion = request.POST.get("descripcion","").strip()
        unidad = request.POST.get("unidad","").strip()
        stock = request.POST.get("stock","").strip()

        # Validación: al menos un campo debe estar lleno
        if not descripcion and not unidad and not stock:
            messages.error(request, "Debes ingresar al menos un dato para actualizar.")
            return redirect("actualizar_inventario_agroquimicos", seleccion=seleccion)

        if descripcion:
            inventario.descripcion = descripcion

        if unidad:
            inventario.unidad = unidad

        if stock:
            inventario.stock = stock

        inventario.save()
        return redirect("inventario_agroquimicos")

    return render(request, 'inventarios/actualizar_agroquimico.html', {'inventario': inventario})


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
    if request.method == 'POST':
        form = Herramientasform(request.POST)

        if form.is_valid():
            Herramientas = form.save(commit=False) 
            Herramientas.tipo = 'Inventario Herramientas'
            Herramientas.categoria = categoria
            Herramientas.save()

            return redirect('inventario_herramientas')  
    else:
        form = Herramientasform()

    return render (request, 'inventarios/registrar_herramienta_maquina.html', {'form': form, 'categoria': categoria})

def actualizar_inventario_herramientas (request,seleccion):
    inventario = get_object_or_404(Inventario, pk=seleccion)

    if request.method == 'POST':
        estado = request.POST.get("estado","").strip()
        stock = request.POST.get("stock","").strip()

        # Validación: al menos un campo debe estar lleno
        if not estado and not stock:
            messages.error(request, "Debes ingresar al menos un dato para actualizar.")
            return redirect("actualizar_inventario_herramientas", seleccion=seleccion)

        if estado:
            inventario.estado = estado

        if stock:
            inventario.stock = stock

        inventario.save()
        return redirect("inventario_herramientas")

    return render(request, 'inventarios/actualizar_herramienta_maquina.html', {'inventario': inventario})

def categoria_herramientas (request):
    return render (request, 'inventarios/categoria_herramienta_maquina.html')
