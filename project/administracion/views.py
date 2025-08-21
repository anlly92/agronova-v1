from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password # Importar hashing seguro
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
import random
import string
from .forms import AdministradorForm
from .models import Administrador
from validaciones import validar_campos_especificos



#importaciones para la busqueda y el filtro
from inventarios.utils import normalizar_texto, es_numero # funciones que se encunetran en utils en la app de inventarios
from django.db.models import Q
from decimal import InvalidOperation 
from administracion.decorators import solo_admin_principal # lo importamos para manejar la proteccion de las rutas si no es administrador principal



def generador_contraseña ():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices (caracteres, k=5))

@solo_admin_principal
def gestionar_administrador(request):
    ok = False
    # Acciones POST
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

        if accion == "borrar":
            ok = True
            admins = Administrador.objects.filter(pk__in=ids)

            for admin in admins:
                correo = admin.correo
                admin.delete()
                from django.contrib.auth.models import User
                User.objects.filter(username=correo).delete()

    # llamamos a la funcion de filtrar administradores
    Administradores, buscar, id_admin, nombre, apellido, telefono, correo = filtrar_administradores(request)
    cantidad_filas_vacias = 15 - Administradores.count()


    contexto = {
        "Administradores": Administradores,
        "filas_vacias": range(cantidad_filas_vacias),
        "buscar": buscar,
        "id_admin": id_admin,
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "correo": correo,        
        "ok": ok,
    }

    return render(request, "administracion/gestionar_administrador.html", contexto)

@solo_admin_principal
def registro_administrador (request):
    ok = False 
    errores = {}

    if request.method == 'POST':
        datos = request.POST
        form = AdministradorForm(datos)

        errores = validar_campos_especificos(post_data=datos)

        for campo, mensaje in errores.items():
            if campo in form.fields:
                form.add_error(campo, mensaje)

        if form.is_valid():
            administrador = form.save(commit=False) 
            # Generar contraseña aleatoria
            contraseña_generada = generador_contraseña()

            # ciframos la contraseña generada
            contraseña_cifrada = make_password(contraseña_generada)

            # Crear objeto User sincronizado (username = correo)
            user = User.objects.create(
                username = administrador.correo,   
                email    = administrador.correo,
                first_name = administrador.nombre,
                last_name  = administrador.apellido,
                password   = contraseña_cifrada ,
                is_staff   = True             
            )

            administrador.contraseña = contraseña_cifrada

            # Guardar administrador
            administrador.save()

            mensaje_html = render_to_string('administracion/mensaje_correo.html',{
                'nombre': administrador.nombre,
                'apellido': administrador.apellido,
                'correo': administrador.correo,
                'contraseña': contraseña_generada
            })

            # Enviar la contraseña por correo
            subject = 'Bienvenido a Agronova'
            from_email = 'agronovaesloni@gmail.com'
            to_email = [administrador.correo]

            email = EmailMultiAlternatives(subject, '', from_email, to_email)
            email.attach_alternative(mensaje_html, "text/html")
            email.send()

            ok = True
    else:
        form = AdministradorForm()
    
    return render (request, 'administracion/registro_administrador.html', {'form': form,'ok':ok})

@login_required
def sobre_mi (request):
    usuario = request.user
    try:
        administrador = Administrador.objects.get(correo=usuario.username)
    except Administrador.DoesNotExist:
        administrador = None  

    return render(request, 'administracion/sobre_mi.html',{'usuario': usuario,'administrador': administrador})

@login_required
def editar_perfil (request):
    if request.method == 'POST':
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")

        if not correo and not telefono:
            messages.error(request, "Debes ingresar al menos un dato (correo o teléfono) para actualizar tu perfil.")
            return redirect("editar_perfil")

        admin = Administrador.objects.get(correo=request.user.username)

        # Solo actualiza si los campos no están vacíos
        if correo:
            admin.correo = correo
            user = request.user
            user.username = correo
            user.email = correo

        if telefono:
            admin.telefono = telefono

        try:
            admin.save()
            if correo:
                user.save()
            return redirect("sobre_mi")

        except IntegrityError as e:
            if "correo" in str(e):
                messages.error(request, "Este correo electrónico ya está registrado.")
            elif "telefono" in str(e):
                messages.error(request, "Este número de teléfono ya está registrado.")
            else:
                messages.error(request, "Ha ocurrido un error al guardar los datos.")
    
    return render(request, 'administracion/editar_perfil.html')

#Vistas para la parte de busqueda en la tabla de administradores


def filtrar_administradores(request):
    buscar = request.GET.get("buscar", "").strip()
    id_admin = request.GET.get("id_admin", "").strip()
    nombre = request.GET.get("nombre", "").strip()
    apellido = request.GET.get("apellido", "").strip()
    telefono = request.GET.get("telefono", "").strip()
    correo = request.GET.get("correo", "").strip()

    Administradores = Administrador.objects.all()

    if buscar:
        buscar_normalizado = normalizar_texto(buscar)
        filtro_numerico = Q()
        filtro_texto = Q()

        if es_numero(buscar_normalizado):
            try:
                filtro_numerico = Q(id_admin=int(buscar_normalizado))
            except (ValueError, TypeError):
                pass

        partes = buscar_normalizado.split()

        # se verifica  que todas las partes estén presentes en nombre o apellido
        for parte in partes:
            filtro_texto &= (
                Q(nombre__icontains=parte) |
                Q(apellido__icontains=parte)
            )

        filtro_contacto = (
            Q(telefono__iexact=buscar_normalizado) |
            Q(correo__iexact=buscar_normalizado)
        )

        # se combinan todos los filtros para que se apliquen segun los datos ingresados 
        Administradores = Administrador.objects.filter(
            filtro_numerico | filtro_texto | filtro_contacto
        )

    return Administradores, buscar, id_admin, nombre, apellido, telefono, correo
