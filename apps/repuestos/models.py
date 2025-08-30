from django.db import models
import uuid

class Repuesto(models.Model):
    id_repuesto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'repuesto'
        verbose_name = "Repuesto"
        verbose_name_plural = "Repuestos"
