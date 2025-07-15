from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password # Importar hashing seguro
import random
import string
from .forms import AdministradorForm
from .models import Administrador


def generador_contraseña ():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices (caracteres, k=10))

def gestionar_administrador (request):
    Administradores = Administrador.objects.all()
    cantidad_filas_vacias = 15 - Administradores.count()
    return render (request, 'administracion/gestionar_administrador.html', {'Administradores': Administradores, 'filas_vacias': range(cantidad_filas_vacias)})

def accion_administrador(request):
    seleccion = request.POST.get("elemento")       # columna seleccionada
    accion = request.POST.get("accion")         # accion enviada "editar" o "borrar"

    if not seleccion:
        # si no se selecciono nada no se ejecuta ninguna accion
        return redirect("gestionar_administrador")

    if accion == "editar":
        # redirige al formulario de edición
        return redirect("editar_administrador", seleccion=seleccion)

    if accion == "borrar":
        # elimina el elemento selecionado
        admin= get_object_or_404(Administrador, pk=seleccion)

        correo = admin.correo

        # Borra el registro de Administrador
        admin.delete()

        # Borra el User que tenga ese correo como username
        from django.contrib.auth.models import User
        User.objects.filter(username=correo).delete()

        return redirect("gestionar_administrador")

    return redirect("gestionar_administrador")

def registro_administrador (request):
    if request.method == 'POST':
        form = AdministradorForm(request.POST)
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

            return redirect('gestionar_administrador')
    else:
        form = AdministradorForm()
    
    return render (request, 'administracion/registro_administrador.html', {'form': form})

def actualizar_administrador (request,seleccion):
    return render (request, 'administracion/actualizar_administrador.html')

def sobre_mi (request):
    return render (request, 'administracion/sobre_mi.html')

def editar_perfil (request):
    return render (request, 'administracion/editar_perfil.html')
