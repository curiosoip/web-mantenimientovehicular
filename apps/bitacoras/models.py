from django.db import models
from apps.vehiculos.models import Vehiculo
from apps.usuarios.models import Usuario
from django.core.exceptions import ValidationError
import uuid

class Bitacora(models.Model):
    id_bitacora = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="bitacoras")
    chofer = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    km_inicial = models.PositiveIntegerField()
    km_final = models.PositiveIntegerField()
    combustible_cargado = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    costo_combustible = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True, null=True)
    foto_odometro_inicio = models.URLField( null=True, blank=True)
    foto_odometro_fin = models.URLField( null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def distancia_recorrida(self):
        return self.km_final - self.km_inicial

    def rendimiento_combustible(self):
        return self.distancia_recorrida() / self.combustible_cargado if self.combustible_cargado > 0 else 0

    def clean(self):
        if self.km_inicial is not None and self.km_final is not None:
            if self.km_final < self.km_inicial:
                raise ValidationError("El kilometraje final no puede ser menor que el inicial.")


    def __str__(self):
        return f"Bitácora {self.vehiculo.placa} - {self.fecha}"

    class Meta:
        db_table = 'bitacora'
        verbose_name = "Bitácora"
        verbose_name_plural = "Bitácoras"
        ordering = ['-fecha']


