from django.db import models
from apps.vehiculos.models import Vehiculo
import uuid

class SolicitudMantenimiento(models.Model):
    id_solicitud_mantenimiento = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="solicitudes")
    fecha_solicitud = models.DateField(auto_now_add=True)
    descripcion = models.TextField()
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("aceite", "Cambio de aceite"),
            ("frenos", "Frenos"),
            ("suspension", "Suspensión"),
            ("llantas", "Llantas"),
            ("bateria", "Batería"),
            ("otro", "Otro")
        ],
        default="otro"
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("aprobado", "Aprobado"),
            ("finalizado", "Finalizado")
        ],
        default="pendiente"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Solicitud {self.vehiculo.placa} - {self.tipo} ({self.estado})"

    class Meta:
        db_table = 'solicitud_mantenimiento'
        verbose_name = "Solicitud de mantenimiento"
        verbose_name_plural = "Solicitudes de mantenimiento"
        ordering = ['-fecha_solicitud']




class OrdenServicio(models.Model):
    id_orden_servicio = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    solicitud = models.OneToOneField(SolicitudMantenimiento, on_delete=models.CASCADE, related_name="orden_servicio")
    fecha_emision = models.DateField(auto_now_add=True)
    proveedor = models.CharField(max_length=100)
    costo_mano_obra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    costo_aceites = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def costo_repuestos(self):
        return sum(detalle.subtotal() for detalle in self.detalle_repuestos.all())

    def total(self):
        return self.costo_mano_obra + self.costo_repuestos() + self.costo_aceites

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Si la solicitud se finaliza, cambiar el estado del vehículo
        if self.solicitud.estado == "finalizado":
            self.solicitud.vehiculo.estado = "activo"
            self.solicitud.vehiculo.save()
        elif self.solicitud.estado == "aprobado":
            self.solicitud.vehiculo.estado = "mantenimiento"
            self.solicitud.vehiculo.save()

    def __str__(self):
        return f"Orden de servicio {self.solicitud.vehiculo.placa}"

    class Meta:
        db_table = 'orden_servicio'
        verbose_name = "Orden de servicio"
        verbose_name_plural = "Órdenes de servicio"
        ordering = ['-fecha_emision']

    
