from django.shortcuts import render

def gestionar_lote (request):
    return render (request, 'cafe_cardamomo/mostrar_lotes.html')

def registrar_lote (request):
    return render (request, 'cafe_cardamomo/registro_lote.html')

def actualizar_lote (request):
    return render (request, 'cafe_cardamomo/actualizar_lote.html')

def gestionar_recoleccion (request):
    return render (request, 'cafe_cardamomo/mostrar_recoleccion.html')

def registrar_recoleccion (request):
    return render (request, 'cafe_cardamomo/registro_recoleccion.html')

def registrar_pago (request):
    return render (request, 'cafe_cardamomo/registrar_pago.html')

def total_de_recoleccion (request):
    return render (request, 'cafe_cardamomo/total_de_recoleccion.html')