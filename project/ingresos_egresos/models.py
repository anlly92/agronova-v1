from django.db import models
from administracion.models import Administrador  # Asegúrate de importar tu modelo correctamente
from inventarios.models import Inventario  

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
    anulada = models.BooleanField(default=False)


    class Meta:
        db_table = 'ingresos_egresos'

    def __str__(self):
        return f"{self.id_admin} - {self.tipo} - {self.descripcion} {self.fecha} - {self.monto}"

class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_admin = models.ForeignKey(Administrador, on_delete=models.CASCADE, db_column='id_admin')
    id_producto = models.ForeignKey(Inventario, on_delete=models.SET_NULL,null=True,blank=True, db_column='id_producto')
    nombre_producto = models.CharField(max_length=255, null=True, blank=True)
    contenido = models.CharField(max_length=100, blank=True, null=True)
    unidad = models.CharField(max_length=50, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    total = models.PositiveIntegerField(null=True, blank=True)
    anulada = models.BooleanField(default=False)

    class Meta:
        db_table = 'ventas'

    def __str__(self):
        return f" {self.id_venta} - {self.id_producto.nombre} - {self.fecha}"