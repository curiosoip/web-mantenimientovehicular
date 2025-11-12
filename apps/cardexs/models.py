from django.db import models
import uuid
from apps.vehiculos.models import Vehiculo

class Cardex(models.Model):
    id_cardex = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE, related_name="cardex")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cardex de {self.vehiculo.placa}"


class RegistroCardex(models.Model):
    id_registro_cardex = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cardex = models.ForeignKey(Cardex, on_delete=models.CASCADE, related_name="registros")
    fecha = models.DateField()
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("mantenimiento", "Mantenimiento"),
            ("combustible", "Combustible"),
            ("otro", "Otro")
        ],
        default="otro"
    )
    descripcion = models.TextField()
    documento_respaldo = models.FileField(upload_to="documentos/", null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cardex.vehiculo.placa} - {self.tipo} ({self.fecha})"

