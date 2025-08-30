from django.db import models
from apps.vehiculos.models import Vehiculo
import uuid

class Mantenimiento(models.Model):
    TIPO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completado', 'Completado'),
    ]
    id_mantenimiento = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    fecha_programada = models.DateField()
    fecha_realizado = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehiculo.placa
    
    class Meta:
        db_table = 'mantenimiento'
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"