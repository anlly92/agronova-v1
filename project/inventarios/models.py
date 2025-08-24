from django.db import models
from cafe_cardamomo.models import Lote 
from django.db import transaction

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

    TALA_CHOICES = [
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
    tala = models.CharField (max_length=2, choices=TALA_CHOICES, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    nombre_lote = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'inventario'

    # Sobrescribimos el método save para aplicar lógica adicional
    def save(self, *args, **kwargs):
        with transaction.atomic():
            is_new = self._state.adding  # Saber si es creación
            super().save(*args, **kwargs)

            if is_new and self.tipo == 'Inventario Arbustos' and self.id_lote:
                lote = self.id_lote
                cantidad = int(self.stock or 0)  # truncar mejor que redondear

                if self.renovacion == "Sí":
                    return  

                if self.tala == "Sí":
                    nueva_cantidad = lote.cantidad_actual - cantidad
                    lote.cantidad_actual = max(nueva_cantidad, 0)
                else:
                    nueva_cantidad = lote.cantidad_actual + cantidad
                    lote.cantidad_actual = min(nueva_cantidad, lote.cantidad_maxima)
                    
                lote.save()

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

    


