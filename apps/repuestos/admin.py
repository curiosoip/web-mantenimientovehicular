from django.contrib import admin
from .models import Repuesto, RepuestoUsado, DevolucionRepuesto




@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo", "precio_unitario", "fecha_registro", "fecha_actualizacion")
    search_fields = ("nombre", "codigo", "descripcion")
    list_filter = ("fecha_registro",)
    ordering = ("nombre",)
    readonly_fields = ("fecha_registro", "fecha_actualizacion")

    actions = ["actualizar_precios"]

    @admin.action(description="Duplicar precios (solo ejemplo)")
    def actualizar_precios(self, request, queryset):
        for repuesto in queryset:
            repuesto.precio_unitario *= 2
            repuesto.save()



@admin.register(RepuestoUsado)
class RepuestoUsadoAdmin(admin.ModelAdmin):
    list_display = ("repuesto", "orden_servicio", "cantidad", "precio_unitario", "subtotal_display", "fecha_registro")
    search_fields = ("repuesto__nombre", "orden_servicio__solicitud__vehiculo__placa")
    list_filter = ("fecha_registro", "repuesto")
    readonly_fields = ("fecha_registro", "fecha_actualizacion")
    ordering = ("-fecha_registro",)
    list_select_related = ("repuesto", "orden_servicio")

    def subtotal_display(self, obj):
        return f"{obj.subtotal():.2f} Bs"
    subtotal_display.short_description = "Subtotal"




@admin.register(DevolucionRepuesto)
class DevolucionRepuestoAdmin(admin.ModelAdmin):
    list_display = ("repuesto", "orden_servicio", "cantidad", "fecha", "observacion")
    search_fields = ("repuesto__nombre", "orden_servicio__solicitud__vehiculo__placa")
    list_filter = ("fecha", "repuesto")
    ordering = ("-fecha",)
    list_select_related = ("repuesto", "orden_servicio")
