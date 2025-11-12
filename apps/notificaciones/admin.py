from django.contrib import admin
from .models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("usuario", "mensaje_resumido", "leido", "fecha", "fecha_registro")
    list_filter = ("leido", "fecha")
    search_fields = ("usuario__username", "mensaje")
    ordering = ("-fecha",)
    readonly_fields = ("fecha", "fecha_registro", "fecha_actualizacion")
    list_select_related = ("usuario",)
    actions = ["marcar_como_leidas", "marcar_como_no_leidas"]

    def mensaje_resumido(self, obj):
        return (obj.mensaje[:60] + "...") if len(obj.mensaje) > 60 else obj.mensaje
    mensaje_resumido.short_description = "Mensaje"

    @admin.action(description="Marcar como leídas")
    def marcar_como_leidas(self, request, queryset):
        updated = queryset.update(leido=True)
        self.message_user(request, f"{updated} notificaciones marcadas como leídas.")

    @admin.action(description="Marcar como no leídas")
    def marcar_como_no_leidas(self, request, queryset):
        updated = queryset.update(leido=False)
        self.message_user(request, f"{updated} notificaciones marcadas como no leídas.")
