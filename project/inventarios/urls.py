from django.urls import path
from inventarios import views

urlpatterns = [
    path("inventario_producto_final/", views.inventario_producto_final, name='inventario_producto_final'),
    path("registrar_inventario_producto_final/", views.registrar_inventario_producto_final, name='registrar_inventario_producto_final'),
    path("actualizar_producto_final/", views.actualizar_producto_final, name='actualizar_producto_final'),
    path("inventario_arbustos/", views.inventario_arbustos, name='inventario_arbustos'),
    path("registrar_inventario_arbustos/", views.registrar_inventario_arbustos, name='registrar_inventario_arbustos'),
    path("actualizar_inventario_arbustos/", views.actualizar_inventario_arbustos, name='actualizar_inventario_arbustos'),
    path("inventario_agroquimicos/", views.inventario_agroquimicos, name='inventario_agroquimicos'),
    path("registrar_inventario_agroquimicos/", views.registrar_inventario_agroquimicos, name='registrar_inventario_agroquimicos'),
    path("actualizar_inventario_agroquimicos/", views.actualizar_inventario_agroquimicos, name='actualizar_inventario_agroquimicos'),
    path("inventario_herramientas/", views.inventario_herramientas, name='inventario_herramientas'),
    path("registrar_herramientas/", views.registrar_herramientas, name='registrar_herramientas'),
    path("actualizar_inventario_herramientas/", views.actualizar_inventario_herramientas, name='actualizar_inventario_herramientas'),
    path("categoria_herramientas/", views.categoria_herramientas, name='categoria_herramientas'),
] 