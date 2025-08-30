from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Mantenimiento
from .forms import MantenimientoForm
from apps.vehiculos.models import Vehiculo

def index(request):
    query = request.GET.get('q', '')
    if query:
        lista_mantenimientos = Mantenimiento.objects.filter(
            Q(vehiculo__placa__icontains=query) |
            Q(tipo__icontains=query) |
            Q(estado__icontains=query) |
            Q(descripcion__icontains=query)
        ).order_by('-fecha_registro')
    else:
        lista_mantenimientos = Mantenimiento.objects.all().order_by('-fecha_registro')

    paginacion = Paginator(lista_mantenimientos, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    context = {
        "banner_title": "Mantenimientos",
        "pagina_actual": pagina_actual,
        "vehiculos": Vehiculo.objects.all(),
        "total_registros": lista_mantenimientos.count(),
        "query": query
    }
    return render(request, 'admin/mantenimientos/index.html', context=context)

def eliminar_mantenimiento(request, id_mantenimiento):
    mantenimiento = get_object_or_404(Mantenimiento, id_mantenimiento=id_mantenimiento)
    try:
        mantenimiento.delete()
    except Exception as e:
        print(f"Error al eliminar el mantenimiento: {str(e)}")

    return redirect('mantenimientos')

def registrar_mantenimiento(request):
    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mantenimientos')
        return redirect('mantenimientos')
    else:
        form = MantenimientoForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Mantenimiento'
    }

    return render(request, 'admin/mantenimientos/index.html', context)
