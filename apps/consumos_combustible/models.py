from django.db import models
from apps.usuarios.models import Usuario
from apps.vehiculos.models import Vehiculo
from apps.bitacoras.models import Bitacora
import uuid

class ConsumoCombustible(models.Model):
    id_consumo_combustible = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="consumos")
    bitacora = models.ForeignKey(Bitacora, on_delete=models.SET_NULL, null=True, blank=True, related_name="consumo")
    chofer = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    litros = models.DecimalField(max_digits=8, decimal_places=2)
    costo = models.DecimalField(max_digits=12, decimal_places=2)
    estacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def rendimiento(self):
        if self.bitacora:
            return self.bitacora.rendimiento_combustible()
        return None

    def __str__(self):
        return f"Consumo {self.vehiculo.placa} - {self.fecha}"

    class Meta:
        db_table = 'consumo_combustible'
        verbose_name = "Consumo de combustible"
        verbose_name_plural = "Consumos de combustible"
        ordering = ['-fecha']
