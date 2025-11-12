from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import SolicitudMantenimiento, OrdenServicio
from .forms import SolicitudMantenimientoForm
from apps.vehiculos.models import Vehiculo
from django.urls import reverse

from apps.usuarios.models import Usuario

# Listado de solicitudes
def index(request):
    query = request.GET.get('q', '')
    user = request.user

    if query:
        lista_solicitudes = SolicitudMantenimiento.objects.filter(
            Q(vehiculo__placa__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(tipo__icontains=query) |
            Q(estado__icontains=query)
        ).order_by('-fecha_solicitud')
    else:
        lista_solicitudes = SolicitudMantenimiento.objects.all().order_by('-fecha_solicitud')

    if user.is_superuser:
        vehiculos = Vehiculo.objects.all().order_by('placa')
    else:
        vehiculos = Vehiculo.objects.filter(departamento=user.departamento).order_by('placa')

    paginacion = Paginator(lista_solicitudes, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    context = {
        "banner_title": "Solicitudes de Mantenimiento",
        "pagina_actual": pagina_actual,
        "total_registros": lista_solicitudes.count(),
        "query": query,
        "vehiculos": vehiculos,
    }
    return render(request, 'admin/mantenimientos/index.html', context=context)


# Eliminar solicitud
def eliminar_solicitud(request, id_solicitud):
    solicitud = get_object_or_404(SolicitudMantenimiento, id_solicitud_mantenimiento=id_solicitud)
    try:
        solicitud.delete()
        messages.success(request, "Solicitud eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la solicitud: {str(e)}")
    return redirect('solicitudes')


# Registrar solicitud
def registrar_solicitud(request):
    if request.method == 'POST':
        form = SolicitudMantenimientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Solicitud registrada correctamente.")
            return redirect('solicitudes')
        else:
            for field, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{field}: {error}")
            return redirect('solicitudes')
    return redirect('solicitudes')


# Detalle de solicitud (opcional, para mostrar info y la orden asociada)
def detalle_solicitud(request, id_solicitud):
    solicitud = get_object_or_404(SolicitudMantenimiento, id_solicitud_mantenimiento=id_solicitud)
    orden = getattr(solicitud, 'orden_servicio', None)
    context = {
        "solicitud": solicitud,
        "orden": orden,
        "banner_title": f"Solicitud {solicitud.vehiculo.placa}"
    }
    return render(request, 'admin/mantenimientos/detalle.html', context=context)


def cambiar_estado_solicitud(request, id_solicitud):
    solicitud = get_object_or_404(SolicitudMantenimiento, pk=id_solicitud)

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        if nuevo_estado in dict(SolicitudMantenimiento._meta.get_field('estado').choices):
            solicitud.estado = nuevo_estado
            solicitud.save()
        return redirect('solicitudes')

    return render(request, "mantenimiento/cambiar_estado_solicitud.html", {"solicitud": solicitud})