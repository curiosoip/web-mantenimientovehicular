from django.db import models
from apps.vehiculos.models import Vehiculo
from apps.usuarios.models import Usuario
from apps.repuestos.models import Repuesto
import uuid

class MovimientoRepuesto(models.Model):
    id_movimiento_repuesto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    ACCION_CHOICES = [
        ('entrega', 'Entrega'),
        ('devolucion', 'Devolución'),
    ]
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    accion = models.CharField(max_length=10, choices=ACCION_CHOICES)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehiculo.placa
    
    class Meta:
        db_table = 'movimiento'
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"