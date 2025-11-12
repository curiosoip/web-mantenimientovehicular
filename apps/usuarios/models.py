from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Usuario(AbstractUser):
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
    ROLES = [
        ('Administrador general', 'Administrador general'),
        ('Jefe de unidad', 'Jefe de unidad'),
        ('Encargado parque motor', 'Encargado parque motor'),
        ('Chofer', 'Chofer'),
        ('Finanzas', 'Finanzas')
    ]
    id_usuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rol = models.CharField(max_length=30, choices=ROLES,default='Chofer')
    departamento = models.CharField(max_length=2, choices=DEPARTAMENTOS, default="LP")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuario'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return  self.username
