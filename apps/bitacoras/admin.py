from django.contrib import admin
from .models import Bitacora


@admin.register(Bitacora)
class BitacoraAdmin(admin.ModelAdmin):
    list_display = (
        "vehiculo",
        "chofer",
        "fecha",
        "km_inicial",
        "km_final",
        "distancia_recorrida",
        "combustible_cargado",
        "costo_combustible",
        "rendimiento_display",
    )
    list_filter = ("fecha", "vehiculo", "chofer")
    search_fields = ("vehiculo__placa", "chofer__username", "observaciones")
    ordering = ("-fecha",)
    readonly_fields = ("fecha_registro", "fecha_actualizacion")
    list_select_related = ("vehiculo", "chofer")

    def distancia_recorrida(self, obj):
        return obj.distancia_recorrida()
    distancia_recorrida.short_description = "Distancia (km)"

    def rendimiento_display(self, obj):
        return f"{obj.rendimiento_combustible():.2f} km/l" if obj.combustible_cargado > 0 else "-"
    rendimiento_display.short_description = "Rendimiento"
