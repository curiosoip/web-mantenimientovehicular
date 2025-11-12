from django.db import models
import uuid
from apps.mantenimientos.models import OrdenServicio
from django.core.exceptions import ValidationError


class Repuesto(models.Model):
    id_repuesto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    codigo = models.CharField(max_length=50, blank=True, null=True, unique=True)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})" if self.codigo else self.nombre

    class Meta:
        db_table = 'repuesto'
        verbose_name = "Repuesto"
        verbose_name_plural = "Repuestos"
        ordering = ['nombre']


class RepuestoUsado(models.Model):
    id_repuesto_usado = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orden_servicio = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE, related_name="detalle_repuestos")
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def subtotal_display(self):
        return f"{self.subtotal():.2f} Bs"

    def __str__(self):
        return f"{self.repuesto.nombre} x{self.cantidad} en {self.orden_servicio}"


class DevolucionRepuesto(models.Model):
    id_devolucion_repuesto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orden_servicio = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE, related_name="devoluciones")
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad de devolución debe ser mayor a cero.")

    def __str__(self):
        return f"Devolución {self.repuesto.nombre} ({self.cantidad}) - {self.orden_servicio}"



