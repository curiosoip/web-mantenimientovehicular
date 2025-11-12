from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ("username", "rol", "departamento", "first_name", "last_name", "email", "fecha_registro", "fecha_actualizacion")
    list_filter = ("rol", "departamento", "is_active", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    readonly_fields = ("fecha_registro", "fecha_actualizacion")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name", "email")}),
        ("Permisos", {"fields": ("rol", "departamento", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas", {"fields": ("fecha_registro", "fecha_actualizacion")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "rol", "departamento"),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(departamento=request.user.departamento)
        return qs
