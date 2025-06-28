from django.shortcuts import render

def gestionar_personal (request):
    return render (request, 'personal/gestionar_personal.html')

def registro_personal (request):
    return render (request, 'personal/registrar_personal.html')

def actualizar_personal (request):
    return render (request, 'personal/actualizar_personal.html')

