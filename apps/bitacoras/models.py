from django.db import models
from apps.vehiculos.models import Vehiculo
from apps.usuarios.models import Usuario
import uuid

class BitacoraViaje(models.Model):
    id_bitacora_viaje = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    conductor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    ruta = models.TextField()
    kilometros_recorridos = models.FloatField()
    observaciones = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehiculo.placa
    
    class Meta:
        db_table = 'bitacora_viaje'
        verbose_name = "Bitacora de viaje"
        verbose_name_plural = "Bitacoras de viajes"