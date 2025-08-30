from django.db import models
from apps.vehiculos.models import Vehiculo
import uuid

class DotacionCombustible(models.Model):
    id_dotacion_combustible = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad_litros = models.FloatField()
    kilometraje_actual = models.FloatField()
    observaciones = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehiculo.placa
    
    class Meta:
        db_table = 'dotacion_combustible'
        verbose_name = "Dotacion Combustible"
        verbose_name_plural = "Dotaciones de Combustible"