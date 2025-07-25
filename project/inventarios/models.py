from django.db import models
from cafe_cardamomo.models import Lote 

class Inventario(models.Model):
    CATEGORIA_CHOICES = [
        ('Herramienta', 'Herramienta'),
        ('Maquina', 'Maquina'),
    ]

    ESTADO_CHOICES = [
        ('Buena', 'Buena'),
        ('Regular', 'Regular'),
        ('Mala', 'Mala'),
    ]

    ARBUSTO_CHOICES = [
        ('Café', 'Café'),
        ('Cardamomo', 'Cardamomo'),
    ]

    RENOVACION_CHOICES = [
        ('Sí', 'Sí'),
        ('No', 'No'),
    ]

    id_inventario = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50,default='Desconocido')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unidad = models.CharField(max_length=50, blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, blank=True, null=True)
    tipo_arbusto = models.CharField(max_length=20, choices=ARBUSTO_CHOICES, blank=True, null=True)
    fecha_siembra = models.DateField(blank=True, null=True)
    renovacion = models.CharField(max_length=2, choices=RENOVACION_CHOICES, blank=True, null=True)
    id_lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_lote')
    contenido = models.CharField(max_length=100, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'inventario'

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"


