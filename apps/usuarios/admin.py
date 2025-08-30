from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('id_usuario', 'username', 'rol', 'is_active', 'is_staff', 'fecha_registro', 'fecha_actualizacion')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-fecha_registro',)
    readonly_fields = ('fecha_registro', 'fecha_actualizacion', 'id_usuario')  

    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('rol',),  
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('rol',),
        }),
    )