from django.db import models
from personal.models import Empleado
from cafe_cardamomo.models import Lote
from inventarios.models import Inventario  

class Proceso(models.Model):
    TIPO_CHOICES = [
        ('Producción', 'Producción'),
        ('Agrícola', 'Agrícola'),
    ]

    PRODUCTO_CHOICES = [
        ('Café', 'Café'),
        ('Cardamomo', 'Cardamomo'),
    ]

    id_proceso = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    tipo_producto = models.CharField(max_length=20, choices=PRODUCTO_CHOICES, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_empleado')
    nombre_empleado = models.CharField(max_length=100, blank=True, null=True)
    id_lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_lote')
    nombre_lote = models.CharField(max_length=100, blank=True, null=True)
    id_inventario = models.ForeignKey(Inventario, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_inventario')
    nombre_agroquimico = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'proceso'

    def __str__(self):
        return f"{self.tipo} - {self.tipo_producto or 'N/A'} - {self.fecha}"
