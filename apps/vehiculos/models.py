from django.db import models
import uuid
from apps.usuarios.models import Usuario
from django.core.exceptions import ValidationError
from django.utils import timezone


class Vehiculo(models.Model):
    DEPARTAMENTOS = [
        ("LP", "La Paz"),
        ("CB", "Cochabamba"),
        ("SC", "Santa Cruz"),
        ("OR", "Oruro"),
        ("PT", "Potosí"),
        ("CH", "Chuquisaca"),
        ("TJ", "Tarija"),
        ("BN", "Beni"),
        ("PD", "Pando"),
    ]
    id_vehiculo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departamento = models.CharField(max_length=2, choices=DEPARTAMENTOS, default="LP")
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    numero_motor = models.CharField(max_length=50, blank=True, null=True)
    numero_chasis = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("activo", "Activo"),
            ("mantenimiento", "En Mantenimiento"),
            ("baja", "Baja")
        ],
        default="activo"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vehiculo'
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['placa']

    @property
    def chofer_asignado(self):
        asignacion = self.asignaciones.filter(fecha_fin__isnull=True).first()
        return asignacion.chofer if asignacion else None


    def __str__(self):
        return f"{self.placa} ({self.marca} {self.modelo})"

    def kilometraje_total(self):
        return self.bitacoras.aggregate(models.Max("km_final"))["km_final__max"] or 0


class AsignacionVehiculo(models.Model):
    id_asignacion_vehiculo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="asignaciones")
    chofer = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Asignación {self.vehiculo.placa} a {self.chofer}"

    @classmethod
    def asignacion_actual(cls, vehiculo):
        return cls.objects.filter(vehiculo=vehiculo, fecha_fin__isnull=True).first()

    def clean(self):
        if self.chofer and self.chofer.departamento != self.vehiculo.departamento:
            raise ValidationError("El chofer debe pertenecer al mismo departamento que el vehículo.")

    class Meta:
        db_table = 'asignacion_vehiculo'
        verbose_name = "Asignación de Vehículo"
        verbose_name_plural = "Asignaciones de Vehículos"