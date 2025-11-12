from django.contrib import admin
from .models import SolicitudMantenimiento, OrdenServicio


@admin.register(SolicitudMantenimiento)
class SolicitudMantenimientoAdmin(admin.ModelAdmin):
    list_display = ("vehiculo", "tipo", "estado", "fecha_solicitud", "descripcion_corta")
    list_filter = ("tipo", "estado", "fecha_solicitud")
    search_fields = ("vehiculo__placa", "descripcion")
    ordering = ("-fecha_solicitud",)
    readonly_fields = ("fecha_solicitud", "fecha_registro", "fecha_actualizacion")

    actions = ["marcar_pendiente", "marcar_aprobada", "marcar_finalizada"]

    def descripcion_corta(self, obj):
        """Muestra los primeros 50 caracteres de la descripción."""
        return (obj.descripcion[:50] + "...") if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = "Descripción"

    @admin.action(description="Marcar como Pendiente")
    def marcar_pendiente(self, request, queryset):
        updated = queryset.update(estado="pendiente")
        self.message_user(request, f"{updated} solicitudes marcadas como Pendiente.")

    @admin.action(description="Marcar como Aprobada")
    def marcar_aprobada(self, request, queryset):
        updated = queryset.update(estado="aprobado")
        self.message_user(request, f"{updated} solicitudes marcadas como Aprobadas.")

    @admin.action(description="Marcar como Finalizada")
    def marcar_finalizada(self, request, queryset):
        updated = queryset.update(estado="finalizado")
        self.message_user(request, f"{updated} solicitudes marcadas como Finalizadas.")



@admin.register(OrdenServicio)
class OrdenServicioAdmin(admin.ModelAdmin):
    list_display = ("solicitud", "vehiculo", "proveedor", "costo_mano_obra", "costo_aceites", "costo_repuestos_display", "total_display", "fecha_emision")
    list_filter = ("fecha_emision", "proveedor")
    search_fields = ("solicitud__vehiculo__placa", "proveedor")
    ordering = ("-fecha_emision",)
    readonly_fields = ("fecha_emision", "fecha_registro", "fecha_actualizacion")

    list_select_related = ("solicitud", "solicitud__vehiculo")

    def vehiculo(self, obj):
        return obj.solicitud.vehiculo
    vehiculo.short_description = "Vehículo"

    def costo_repuestos_display(self, obj):
        return f"{obj.costo_repuestos():.2f} Bs"
    costo_repuestos_display.short_description = "Costo Repuestos"

    def total_display(self, obj):
        return f"{obj.total():.2f} Bs"
    total_display.short_description = "Total"
