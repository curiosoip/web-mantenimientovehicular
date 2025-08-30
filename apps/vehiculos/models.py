from django.db import models
import uuid

class Vehiculo(models.Model):
    id_vehiculo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    tipo = models.CharField(max_length=50)
    estado_actual = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.placa
    
    class Meta:
        db_table = 'vehiculo'
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"
