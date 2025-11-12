from django.contrib import admin
from .models import Cardex, RegistroCardex



class RegistroCardexInline(admin.TabularInline):
    model = RegistroCardex
    extra = 0
    readonly_fields = ("fecha_registro", "fecha_actualizacion")
    fields = ("fecha", "tipo", "descripcion", "documento_respaldo", "fecha_registro", "fecha_actualizacion")
    show_change_link = True




@admin.register(Cardex)
class CardexAdmin(admin.ModelAdmin):
    list_display = ("vehiculo", "creado", "actualizado", "total_registros")
    search_fields = ("vehiculo__placa",)
    readonly_fields = ("creado", "actualizado", "fecha_registro", "fecha_actualizacion")
    ordering = ("vehiculo__placa",)
    inlines = [RegistroCardexInline]

    def total_registros(self, obj):
        return obj.registros.count()
    total_registros.short_description = "Total de registros"



