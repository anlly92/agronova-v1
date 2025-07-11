from django.db import models

class Administrador(models.Model):
    id_admin = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True) 
    contraseña = models.CharField(max_length=255, blank=True, null=True)
    es_principal = models.BooleanField(default=False)

    class Meta:
        db_table = 'administrador'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

