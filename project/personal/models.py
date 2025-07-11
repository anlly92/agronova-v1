from django.db import models

class Empleado(models.Model):
    TIPO_EMPLEADO_CHOICES = [
        ('Vinculado', 'Vinculado'),
        ('No vinculado', 'No vinculado'),
    ]

    id_empleado = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    tipo_empleado = models.CharField(max_length=15, choices=TIPO_EMPLEADO_CHOICES)
    pago_contrato = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'empleado'  # Nombre exacto de la tabla

    def __str__(self):
        return f"{self.id_empleado} - {self.nombre} {self.apellido} - {self.tipo_empleado} - {self.telefono} - {self.pago_contrato}"

