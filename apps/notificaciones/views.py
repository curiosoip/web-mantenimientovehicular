from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Notificacion
from apps.usuarios.models import Usuario
from .forms import NotificacionForm

def index(request):
    query = request.GET.get('q','')  # Búsqueda opcional

    if query:
        lista_notificaciones = Notificacion.objects.select_related('usuario').filter(
            Q(mensaje__icontains=query) |
            Q(usuario__username__icontains=query)
        ).order_by('-fecha')
    else:
        lista_notificaciones = Notificacion.objects.select_related('usuario').all().order_by('-fecha')

    paginacion = Paginator(lista_notificaciones, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    lista_usuarios = Usuario.objects.all().order_by('username')

    context = {
        "banner_title": "Notificaciones",
        "pagina_actual": pagina_actual,
        "total_registros": lista_notificaciones.count(),
        "query": query,
        "usuarios": lista_usuarios,  
    }
    return render(request, 'admin/notificaciones/index.html', context=context)


def eliminarnotificacion(request, id_notificacion):
    notificacion = get_object_or_404(Notificacion, id_notificacion=id_notificacion)
    try:
        notificacion.delete()
        messages.success(request, "Notificación eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la notificación: {str(e)}")
    
    return redirect('notificaciones')


def registrar_notificacion(request):
    if request.method == 'POST':
        form = NotificacionForm(request.POST)
        if form.is_valid():
            try:
                notificacion = form.save(commit=False)
                notificacion.save()
                messages.success(request, "Notificación registrada correctamente.")
                return redirect('notificaciones')
            except Exception as e:
                messages.error(request, f"Error al registrar la notificación: {str(e)}")
                return redirect('notificaciones')
        else:
            for field, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{field}: {error}")
            return redirect('notificaciones')
    else:
        form = NotificacionForm()

    context = {
        'form': form,
        'banner_title': 'Crear Notificación'
    }
    return render(request, 'admin/notificaciones/index.html', context)

def marcar_leida(request, id_notificacion):
    notificacion = get_object_or_404(Notificacion, id_notificacion=id_notificacion)
    notificacion.marcar_como_leida()
    return redirect('notificaciones') 