from django.db import models
from administracion.models import Administrador  # Asegúrate de importar tu modelo correctamente

class IngresosEgresos(models.Model):
    TIPO_CHOICES = [
        ('Ingreso', 'Ingreso'),
        ('Egreso', 'Egreso'),
    ]

    id_transaccion = models.AutoField(primary_key=True)
    id_admin = models.ForeignKey(Administrador, on_delete=models.CASCADE, db_column='id_admin')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ingresos_egresos'

    def __str__(self):
        return f"{self.id_admin} - {self.tipo} - {self.descripcion} {self.fecha} - {self.monto}"
