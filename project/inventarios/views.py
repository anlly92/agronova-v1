import traceback
from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProductoFinalform, Arbustosform, Agroquimicosform, Herramientasform
from .models import Inventario
from django.contrib import messages
from.models import Lote
from validaciones import validar_campos_especificos


# importaciones para la usqueda
from django.shortcuts import render # renderizar plantillas HTML desde las vistas
from django.db.models import Q # realizar consultas con condiciones "OR" (|) y "AND" (&) en filtros de Django.
from inventarios.utils import parsear_fecha,normalizar_texto, es_numero # funciones que se encunetran en utils

from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required



# ────────── Producto final ──────────
@login_required
def inventario_producto_final(request):
    ok = False 
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
            Inventario.objects.filter(pk__in=ids).delete()

        elif accion == "editar" and len(ids) == 1:
            ok = True
            return redirect("actualizar_producto_final", seleccion=ids[0])

    producto_final, buscar, nombre, contenido, unidad, precio_unitario, stock = filtrar_producto_final(request)
    cantidad_filas_vacias = 15 - producto_final.count()

    contexto = {
        'producto_final': producto_final,
        'filas_vacias': range(cantidad_filas_vacias),
        'buscar': buscar,
        'filtro_nombre': nombre,
        'filtro_contenido': contenido,
        'filtro_unidad': unidad,
        'filtro_precio_unitario': precio_unitario,
        'filtro_stock': stock,
        "ok": ok,
    }

    return render(request, 'inventarios/inventario_producto_final.html', contexto )


def registrar_inventario_producto_final (request):
    ok = False 
    errores = {}
    if request.method == 'POST':
        datos = request.POST
        form = ProductoFinalform(datos)
        
        errores = validar_campos_especificos(post_data=datos)

        for campo, mensaje in errores.items():
            if campo in form.fields:
                form.add_error(campo, mensaje)

        if form.is_valid():
            ProductoFinal = form.save(commit=False) 
            ProductoFinal.tipo = 'Inventario Producto final'
            ProductoFinal.save()
            ok = True   
    else:
        form = ProductoFinalform()

    return render (request, 'inventarios/registrar_inventario_producto_final.html', {'form': form,'ok':ok})

@login_required
def actualizar_producto_final (request,seleccion):
    ok = False
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
        ok = True

    return render(request, 'inventarios/actualizar_producto_final.html', {'inventario': inventario, 'ok': ok})




def filtrar_producto_final(request):
    producto_final = Inventario.objects.filter(tipo='Inventario Producto final')

    buscar = request.GET.get("buscar", "").strip()
    nombre = request.GET.get("nombre", "").strip()
    contenido = request.GET.get("contenido", "").strip()
    unidad = request.GET.get("unidad", "").strip()
    precio_unitario = request.GET.get("precio_unitario", "").strip()
    stock = request.GET.get("stock", "").strip()


    if buscar:
        buscar_normalizado =  normalizar_texto(buscar)
        filtro_numerico = Q()
        filtro_texto = Q()
        #Se filtra si lo ingresado es exacto
        if es_numero(buscar_normalizado):
            try:
                filtro_numerico = (
                    Q(id_inventario=int(buscar_normalizado))|
                    Q(contenido__iexact=buscar_normalizado)|
                    Q(precio_unitario=float(buscar_normalizado))|
                    Q(stock=int(buscar_normalizado))
                )

            except(ValueError, InvalidOperation):
                pass

        filtro_texto = (
            Q(nombre__iexact=buscar_normalizado)|
            Q(descripcion__iexact=buscar_normalizado)|
            Q(unidad__iexact=buscar_normalizado)
        )

        producto_final = Inventario.objects.filter(
            Q(tipo='Inventario Producto final') & (filtro_numerico |filtro_texto)
            )


    if nombre:
        producto_final = producto_final.filter(nombre__icontains=nombre)

    if contenido:
        producto_final = producto_final.filter(contenido__iexact=contenido)

    if unidad:
        producto_final = producto_final.filter(unidad__iexact=unidad)

    if stock:
        try:
            stock_float = float(stock)
            producto_final = producto_final.filter(stock=stock_float)
        except ValueError:
            pass

    if precio_unitario:
        try:
            precio_float = float(precio_unitario)
            producto_final = producto_final.filter(precio_unitario=precio_float)
        except ValueError:
            pass

    return producto_final, buscar, nombre, contenido, unidad, precio_unitario, stock
# ────────── Arbustos ──────────
@login_required
def inventario_arbustos(request):
    ok = False
    # Para acciones de editar/borrar
    if request.method == "POST" :
        
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
            Inventario.objects.filter(pk__in=ids).delete()

        elif accion == "editar" and len(ids) == 1 :
            ok = True
            return redirect("actualizar_inventario_arbustos", seleccion=ids[0])

    arbustos, lotes, buscar, tipo_arbusto, nombre_lote, nombre, stock, fecha_siembra, renovacion = filtrar_arbustos(request)
    cantidad_filas_vacias = 15 - arbustos.count()
    contexto= {
        'arbustos': arbustos,
        'lote': lotes,
        'filas_vacias': range(cantidad_filas_vacias),
        # Para mantener valores
        'buscar': buscar,
        'filtro_tipo_arbusto': tipo_arbusto,
        'filtro_nombre_lote': nombre_lote,
        'filtro_nombre': nombre,
        'filtro_stock': stock,
        'filtro_fecha_siembra': fecha_siembra,
        'filtro_renovacion': renovacion,
        'ok': ok,
    }

    return render(request, 'inventarios/inventario_arbustos.html',contexto )

@login_required
def registrar_inventario_arbustos (request):
    ok = False 
    errores = {}

    if request.method == 'POST':
        datos = request.POST
        form = Arbustosform(datos)

        errores = validar_campos_especificos(post_data=datos)

        for campo, mensaje in errores.items():
            if campo in form.fields:
                form.add_error(campo, mensaje)

        if form.is_valid():
            Arbusto = form.save(commit=False) 
            Arbusto.tipo = 'Inventario Arbustos'
            
            if Arbusto.id_lote:
                Arbusto.nombre_lote = Arbusto.id_lote.nombre
                
            Arbusto.save()
            ok = True
    else:
        form = Arbustosform()

    lotes = Lote.objects.all()
    return render (request, 'inventarios/registrar_inventario_arbustos.html', {'form': form,'ok':ok, 'lotes': lotes})


@login_required
def actualizar_inventario_arbustos (request,seleccion):
    ok = False
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
        ok = True

    return render(request, 'inventarios/actualizar_arbustos.html', {'inventario': inventario, 'ok': ok})


def filtrar_arbustos(request):
    buscar = request.GET.get("buscar", "").strip()

    tipo_arbusto = request.GET.get("tipo_arbusto", "")
    nombre_lote = request.GET.get("nombre_lote", "")
    nombre = request.GET.get("nombre", "")
    stock = request.GET.get("stock", "")
    fecha_siembra = request.GET.get("fecha_siembra", "")
    renovacion = request.GET.get("renovacion", "")

    arbustos = Inventario.objects.filter(tipo='Inventario Arbustos')
    lotes = Lote.objects.all()

    if buscar:
        buscar_normalizado = normalizar_texto(buscar)
        filtro_numerico = Q()
        filtro_texto = Q()
        filtro_fecha = Q()

        # Filtro numérico
        if es_numero(buscar_normalizado):
            try:
                filtro_numerico = (
                    Q(id_inventario=int(buscar_normalizado)) |
                    Q(stock=float(buscar_normalizado))|
                    Q(id_lote__id_lote__iexact=buscar_normalizado) 

                )
            except (ValueError, InvalidOperation):
                pass

        filtro_texto = (
            Q(renovacion__iexact=buscar_normalizado)|
            Q(nombre__icontains=buscar_normalizado) |
            Q(tipo_arbusto__icontains=buscar_normalizado) |
            Q(id_lote__nombre__icontains=buscar_normalizado)
        )

        fecha_parseada = parsear_fecha(buscar)
        if fecha_parseada:
            filtro_fecha = Q(fecha_siembra=fecha_parseada)

        # Aplicar búsqueda combinada
        arbustos = arbustos.filter(
            filtro_numerico | filtro_texto | filtro_fecha
        )
    # Aplicar filtros del modal
    if tipo_arbusto:
        arbustos = arbustos.filter(tipo_arbusto__iexact=tipo_arbusto)
    if nombre_lote:
        arbustos = arbustos.filter(id_lote__nombre__icontains=nombre_lote)
    if nombre:
        arbustos = arbustos.filter(nombre__icontains=nombre)
    if stock:
        arbustos = arbustos.filter(stock=stock)
    if fecha_siembra:
        arbustos = arbustos.filter(fecha_siembra=fecha_siembra)
    if renovacion:
        arbustos = arbustos.filter(renovacion__iexact=renovacion)
    return arbustos, lotes, buscar, tipo_arbusto, nombre_lote, nombre, stock, fecha_siembra, renovacion 

# ────────── Agroquímicos ──────────
@login_required
def inventario_agroquimicos(request):
    ok = False
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
            Inventario.objects.filter(pk__in=ids).delete()

        elif accion == "editar" and len(ids) == 1:
            ok = True
            return redirect("actualizar_inventario_agroquimicos", seleccion=ids[0])

    agroquimicos, buscar, nombre, contenido, unidad, stock = filtrar_agroquimicos(request)
    cantidad_filas_vacias = 15 - agroquimicos.count()

    contexto = {
        'agroquimicos': agroquimicos,
        'filas_vacias': range(cantidad_filas_vacias),
        'buscar': buscar,

        # valores del filtro que se mantienen
        'filtro_nombre': nombre,
        'filtro_contenido': contenido,
        'filtro_unidad': unidad,
        'filtro_stock': stock,
        'ok': ok,
    }

    return render(request, 'inventarios/inventario_agroquimicos.html',contexto )

@login_required
def registrar_inventario_agroquimicos (request):
    ok = False 
    errores = {}

    if request.method == 'POST':
        datos = request.POST
        form = Agroquimicosform(datos)

        errores = validar_campos_especificos(post_data=datos)

        for campo, mensaje in errores.items():
            if campo in form.fields:
                form.add_error(campo, mensaje)

        if form.is_valid():
            Agroquimicos = form.save(commit=False) 
            Agroquimicos.tipo = 'Inventario Agroquimicos'
            Agroquimicos.save()
            ok = True   
    else:
        form = Agroquimicosform()

    return render (request, 'inventarios/registrar_inventario_agroquimicos.html', {'form': form,'ok':ok})

@login_required
def actualizar_inventario_agroquimicos (request,seleccion):
    ok = False
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
        ok = True

    return render(request, 'inventarios/actualizar_agroquimico.html', {'inventario': inventario, 'ok': ok})



def filtrar_agroquimicos(request):
    nombre = request.GET.get("nombre", "").strip()
    contenido = request.GET.get("contenido", "").strip()
    unidad = request.GET.get("unidad", "").strip()
    stock = request.GET.get("stock", "").strip()
    buscar = request.GET.get("buscar", "").strip()

    agroquimicos = Inventario.objects.filter(tipo='Inventario Agroquimicos')

    buscar_normalizado = normalizar_texto(buscar)

    if buscar:
        filtro_numerico = Q()
        filtro_texto = Q()

        if es_numero(buscar_normalizado):
            try:
                filtro_numerico = (
                    Q(id_inventario=int(buscar_normalizado)) |
                    Q(stock=int(buscar_normalizado)) |
                    Q(contenido=buscar_normalizado)  
                )
            except (ValueError, InvalidOperation):
                pass

        filtro_texto = (
            Q(nombre__iexact=buscar_normalizado) |
            Q(descripcion__icontains=buscar_normalizado) |
            Q(unidad__iexact=buscar_normalizado)
        )
        agroquimicos = agroquimicos.filter(filtro_numerico | filtro_texto)


    if nombre:
        agroquimicos = agroquimicos.filter(nombre__iexact=nombre)
    if contenido:
        agroquimicos = agroquimicos.filter(contenido__iexact=contenido)
    if unidad:
        agroquimicos = agroquimicos.filter(unidad__iexact=unidad)
    if stock:
        agroquimicos = agroquimicos.filter(stock=stock)

    return agroquimicos, buscar, nombre, contenido, unidad, stock
# ────────── Herramientas ──────────
@login_required
def inventario_herramientas(request):
    ok = False
    if request.method == "POST":

        seleccion = request.POST.get("elemento")
        accion = request.POST.get("accion") 
        print("REQUEST POST:", request.POST)
        
        if seleccion:
            if "," in seleccion:
                ids = seleccion.split(",")
            else:
                ids = [seleccion]
        else:
            ids = []

        ids = [int(x) for x in ids if x.strip().isdigit()]

        # acción enviada "editar" o "borrar"
        if accion == "borrar" and ids:
            ok = True
            Inventario.objects.filter(pk__in=ids).delete()
            
        elif accion == "editar" and len(ids) == 1:
            ok = True
            return redirect("actualizar_inventario_herramientas", seleccion=ids[0]) 
        
    herramientas, buscar, categoria, nombre, estado, stock = filtrar_herramientas(request)
    cantidad_filas_vacias = 15 - herramientas.count()
    contexto = {
        'herramientas': herramientas,
        'filas_vacias': range(cantidad_filas_vacias),
        'buscar': buscar,
        # para mantener valores de los filtros en la plantilla
        'filtro_categoria': categoria,
        'filtro_nombre': nombre,
        'filtro_estado': estado,
        'filtro_stock': stock,
        "ok": ok,  # para mostrar mensajes de éxito o error
    }
    return render(request, 'inventarios/inventario_herramientas.html',contexto )

@login_required
def registrar_herramientas (request, categoria):
    ok = False
    errores = {}

    if request.method == 'POST':
        datos = request.POST
        form = Herramientasform(datos)

        errores = validar_campos_especificos(post_data=datos)

        for campo, mensaje in errores.items():
            if campo in form.fields:
                form.add_error(campo, mensaje)

        if form.is_valid():
            Herramientas = form.save(commit=False) 
            Herramientas.tipo = 'Inventario Herramientas'
            Herramientas.categoria = categoria
            Herramientas.save()
            ok = True   
    else:
        form = Herramientasform()

    return render (request, 'inventarios/registrar_herramienta_maquina.html', {'form': form, 'categoria': categoria,'ok':ok})


@login_required
def actualizar_inventario_herramientas (request,seleccion):
    ok = False
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
        ok = True

    return render(request, 'inventarios/actualizar_herramienta_maquina.html', {'inventario': inventario, 'ok': ok})

@login_required
def categoria_herramientas (request):
    return render (request, 'inventarios/categoria_herramienta_maquina.html')

def filtrar_herramientas(request):
    categoria = request.GET.get("categoria", "")
    nombre = request.GET.get("nombre", "")
    estado = request.GET.get("estado", "")
    stock = request.GET.get("stock", "")
    buscar = request.GET.get("buscar", "").strip()

    herramientas = Inventario.objects.filter(tipo='Inventario Herramientas')

    # Filtro de búsqueda general
    if buscar:
        buscar_normalizado = normalizar_texto(buscar)
        filtro_numerico = Q()
        filtro_texto = Q()

        if es_numero(buscar_normalizado):
            try:
                filtro_numerico =(
                Q(id_inventario__iexact=buscar_normalizado) |
                Q(stock=int(buscar_normalizado))
                )
            except (ValueError, InvalidOperation):
                filtro_numerico = Q()

        filtro_texto = (
            Q(nombre__iexact=buscar_normalizado) |
            Q(categoria__iexact=buscar_normalizado) |
            Q(estado__iexact=buscar_normalizado)
        )

        herramientas = herramientas.filter(filtro_numerico | filtro_texto)


    if categoria:
        herramientas = herramientas.filter(categoria__iexact=categoria)
    if nombre:
        herramientas = herramientas.filter(nombre__iexact=nombre)
    if estado:
        herramientas = herramientas.filter(estado__iexact=estado)
    if stock:
        herramientas = herramientas.filter(stock=stock)

    return herramientas, buscar, categoria, nombre, estado, stock

