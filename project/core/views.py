from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def mostrar_home(request):
    return render (request,'core/home_principal.html')

def mostrar_login(request):
    return render ( request, 'core/login.html')

@login_required(login_url='login')
def mostrar_inicio(request):
    return render ( request, 'core/index_administrador.html')

def que_es_agronova (request):
    return render (request, 'core/que_es_agronova.html')

def como_surgio (request):
    return render (request, 'core/como_surgio.html')

def ventajas (request):
    return render (request, 'core/ventajas.html')

def mision_y_vision_agronova (request):
    return render (request, 'core/mision_agronova.html')

def historia (request):
    return render (request, 'core/historia.html')

def mision_y_vision_elisa (request):
    return render (request, 'core/mision_elisa.html')

def contraseña (request):
    return render (request, 'core/contraseña.html')

def terminos_condiciones (request):
    return render (request, 'core/terminos_condiciones.html')








