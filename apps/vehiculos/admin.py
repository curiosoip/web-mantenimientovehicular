from django.contrib import admin
from .models import Vehiculo, AsignacionVehiculo
from apps.usuarios.models import Usuario
from django.utils import timezone


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("placa", "marca", "modelo", "anio", "estado", "departamento", "fecha_registro", "fecha_actualizacion")
    list_filter = ("estado", "marca", "anio", "departamento")
    search_fields = ("placa", "marca", "modelo", "numero_motor", "numero_chasis")
    ordering = ("placa",)
    readonly_fields = ("fecha_registro", "fecha_actualizacion")
    actions = ["marcar_como_activo", "marcar_en_mantenimiento", "marcar_como_baja"]

    @admin.action(description="Marcar vehículo como Activo")
    def marcar_como_activo(self, request, queryset):
        queryset.update(estado="activo")

    @admin.action(description="Marcar vehículo como En Mantenimiento")
    def marcar_en_mantenimiento(self, request, queryset):
        queryset.update(estado="mantenimiento")

    @admin.action(description="Marcar vehículo como Baja")
    def marcar_como_baja(self, request, queryset):
        queryset.update(estado="baja")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and hasattr(request.user, "departamento"):
            return qs.filter(departamento=request.user.departamento)
        return qs


@admin.register(AsignacionVehiculo)
class AsignacionVehiculoAdmin(admin.ModelAdmin):
    list_display = ("vehiculo", "chofer", "fecha_inicio", "fecha_fin", "vigente")
    list_filter = ("fecha_inicio", "fecha_fin", "chofer", "vehiculo__departamento")
    search_fields = ("vehiculo__placa", "chofer__username", "chofer__first_name", "chofer__last_name")
    ordering = ("-fecha_inicio",)
    list_select_related = ("vehiculo", "chofer")

    def vigente(self, obj):
        hoy = timezone.now().date()
        return obj.fecha_inicio <= hoy and (obj.fecha_fin is None or obj.fecha_fin >= hoy)
    
    vigente.boolean = True
    vigente.short_description = "Asignación vigente"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and hasattr(request.user, "departamento"):
            return qs.filter(vehiculo__departamento=request.user.departamento)
        return qs
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  
            return ("fecha_inicio", "fecha_fin")
        return ()


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "chofer":
            kwargs["queryset"] = Usuario.objects.filter(rol="Chofer")  
        return super().formfield_for_foreignkey(db_field, request, **kwargs)