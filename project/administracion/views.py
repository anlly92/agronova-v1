from django.shortcuts import render

def gestionar_administrador (request):
    return render (request, 'administracion/gestionar_administrador.html')

def registro_administrador (request):
    return render (request, 'administracion/registro_administrador.html')

def actualizar_administrador (request):
    return render (request, 'administracion/actualizar_administrador.html')

def sobre_mi (request):
    return render (request, 'administracion/sobre_mi.html')

def editar_perfil (request):
    return render (request, 'administracion/editar_perfil.html')
