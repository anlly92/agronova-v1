from django.shortcuts import render, redirect,get_object_or_404
from .forms import IngresosEgresosform,VentasForm
from .models import IngresosEgresos,Ventas
from administracion.models import Administrador
from inventarios.models import Inventario
from django.contrib.auth.models import User

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

def informe_anual (request):
    return render (request, 'ingresos_egresos/informe_anual.html')

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