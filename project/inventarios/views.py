from django.shortcuts import render

def inventario_producto_final (request):
    return render (request, 'inventarios/inventario_producto_final.html')

def registrar_inventario_producto_final (request):
    return render (request, 'inventarios/registrar_inventario_producto_final.html')

def actualizar_producto_final (request):
    return render (request, 'inventarios/actualizar_producto_final.html')

def inventario_arbustos (request):
    return render (request, 'inventarios/inventario_arbustos.html')

def registrar_inventario_arbustos (request):
    return render (request, 'inventarios/registrar_inventario_arbustos.html')

def actualizar_inventario_arbustos (request):
    return render (request, 'inventarios/actualizar_arbustos.html')

def inventario_agroquimicos (request):
    return render (request, 'inventarios/inventario_agroquimicos.html')

def registrar_inventario_agroquimicos (request):
    return render (request, 'inventarios/registrar_inventario_agroquimicos.html')

def actualizar_inventario_agroquimicos (request):
    return render (request, 'inventarios/actualizar_agroquimico.html')

def inventario_herramientas (request):
    return render (request, 'inventarios/inventario_herramientas.html')

def registrar_herramientas (request):
    return render (request, 'inventarios/registrar_herramienta_maquina.html')

def actualizar_inventario_herramientas (request):
    return render (request, 'inventarios/actualizar_herramienta_maquina.html')

def categoria_herramientas (request):
    return render (request, 'inventarios/categoria_herramienta_maquina.html')
