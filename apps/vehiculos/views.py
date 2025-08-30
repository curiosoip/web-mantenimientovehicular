from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Vehiculo
from .forms import VehiculoForm  # Asegúrate de tener este formulario creado

def index(request):
    query = request.GET.get('q', '')
    if query:
        lista_vehiculos = Vehiculo.objects.filter(
            Q(placa__icontains=query) |
            Q(marca__icontains=query) |
            Q(modelo__icontains=query) |
            Q(tipo__icontains=query) |
            Q(estado_actual__icontains=query)
        ).order_by('-fecha_registro')
    else:
        lista_vehiculos = Vehiculo.objects.all().order_by('-fecha_registro')

    paginacion = Paginator(lista_vehiculos, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    context = {
        "banner_title": "Vehículos",
        "pagina_actual": pagina_actual,
        "total_registros": lista_vehiculos.count(),
        "query": query
    }
    return render(request, 'admin/vehiculos/index.html', context=context)

def eliminar_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=id_vehiculo)
    try:
        vehiculo.delete()
    except Exception as e:
        print(f"Error al eliminar el vehículo: {str(e)}")
    
    return redirect('vehiculos')

def registrar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehiculos')
        else:
            # Renderiza el mismo template con los errores
            context = {
                'form': form,
                'banner_title': 'Registrar Vehículo',
            }
            return render(request, 'admin/vehiculos/index.html', context)
    else:
        form = VehiculoForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Vehículo'
    }

    return render(request, 'admin/vehiculos/index.html', context)
