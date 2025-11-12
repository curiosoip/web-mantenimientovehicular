from django.contrib import admin
from .models import ConsumoCombustible



@admin.register(ConsumoCombustible)
class ConsumoCombustibleAdmin(admin.ModelAdmin):
    list_display = ("vehiculo", "chofer", "bitacora", "fecha", "litros", "costo", "estacion", "rendimiento_display")
    list_filter = ("fecha", "vehiculo", "chofer")
    search_fields = ("vehiculo__placa", "chofer__username", "estacion")
    ordering = ("-fecha",)
    readonly_fields = ("fecha_registro", "fecha_actualizacion")
    list_select_related = ("vehiculo", "chofer", "bitacora")

    def rendimiento_display(self, obj):
        """Muestra el rendimiento si existe la bitácora asociada"""
        rendimiento = obj.rendimiento()
        return f"{rendimiento:.2f}" if rendimiento else "-"
    rendimiento_display.short_description = "Rendimiento"
