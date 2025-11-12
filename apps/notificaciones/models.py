from django.db import models
from apps.usuarios.models import Usuario
import uuid

class Notificacion(models.Model):
    id_notificacion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="notificaciones")
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def marcar_como_leida(self):
        self.leido = True
        self.save()

    def __str__(self):
        return f"Notificación para {self.usuario.username} - {self.fecha}"

    class Meta:
        indexes = [models.Index(fields=['leido', 'fecha'])]
        ordering = ['-fecha']


