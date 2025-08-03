from django.db import models
from personal.models import Empleado


class Lote(models.Model):
    TIPO_ARBUSTO_CHOICES = [
        ('Café', 'Café'),
        ('Cardamomo', 'Cardamomo'),
    ]

    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    id_lote = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=100)
    hectareas = models.FloatField()
    tipo_arbusto = models.CharField(max_length=20, choices=TIPO_ARBUSTO_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')

    class Meta:
        db_table = 'lote'  # Asegura el nombre exacto de la tabla

    def __str__(self):
        return f"{self.nombre} ({self.tipo_arbusto}) - {self.estado}"

class Recoleccion(models.Model):
    TIPO_PRODUCTO_CHOICES = [
        ('Café', 'Café'),
        ('Cardamomo', 'Cardamomo'),
    ]

    id_recoleccion = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='id_empleado')
    id_lote = models.ForeignKey(Lote, on_delete=models.CASCADE, db_column='id_lote')
    tipo_producto = models.CharField(max_length=20, choices=TIPO_PRODUCTO_CHOICES)
    kilos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_pago = models.ForeignKey('Pagos', to_field='tipo_pago', on_delete=models.CASCADE, db_column='tipo_pago')
    horas_trabajadas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'recoleccion'

    def __str__(self):
        return f"{self.id_recoleccion} - {self.id_empleado} - {self.id_lote} - {self.tipo_producto} - {self.kilos} - {self.fecha} - {self.tipo_pago} - {self.horas_trabajadas}"
    
    def calcular_total(self):
        if self.tipo_pago.tipo_pago == 'Horas':
            return self.horas_trabajadas * self.tipo_pago.valor
        elif self.tipo_pago.tipo_pago == 'Kilos':
            return self.kilos * self.tipo_pago.valor
        return 0

class Pagos(models.Model):
    TIPO_PAGO_CHOICES = [
        ('Horas', 'Horas'),
        ('Kilos', 'Kilos'),
    ]

    tipo_pago = models.CharField(
        max_length=10,
        choices=TIPO_PAGO_CHOICES,
        primary_key=True
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'pagos'  

    def __str__(self):
        return f"{self.tipo_pago} - {self.valor if self.valor is not None else 'Sin valor'}"