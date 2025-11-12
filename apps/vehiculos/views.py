from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Vehiculo,AsignacionVehiculo
from .forms import VehiculoForm 
from django.contrib import messages
from django.utils import timezone
from apps.usuarios.models import Usuario



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
    choferes = Usuario.objects.filter(rol='Chofer', is_active=True).order_by('first_name')


    context = {
        "banner_title": "Vehículos",
        "pagina_actual": pagina_actual,
        "total_registros": lista_vehiculos.count(),
        "query": query,
        "choferes": choferes,
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


def cambiar_estado_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=id_vehiculo)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Vehiculo._meta.get_field('estado').choices):
            vehiculo.estado = nuevo_estado
            vehiculo.save()
            messages.success(request, f"Estado del vehículo {vehiculo.placa} actualizado correctamente a {vehiculo.get_estado_display()}.")
        else:
            messages.error(request, "Estado no válido.")
        return redirect('vehiculos')
    

def asignar_vehiculo(request, id_vehiculo):  # <-- cambiar el nombre
    vehiculo = get_object_or_404(Vehiculo, pk=id_vehiculo)

    if request.method == 'POST':
        chofer_id = request.POST.get('chofer')
        chofer = get_object_or_404(Usuario, pk=chofer_id)

        if chofer.departamento != vehiculo.departamento:
            messages.error(request, "El chofer debe pertenecer al mismo departamento que el vehículo.")
            return redirect('vehiculos')

        asign_actual = AsignacionVehiculo.asignacion_actual(vehiculo)
        if asign_actual:
            asign_actual.fecha_fin = timezone.now().date()
            asign_actual.save()

        nueva_asign = AsignacionVehiculo.objects.create(
            vehiculo=vehiculo,
            chofer=chofer,
            fecha_inicio=timezone.now().date()
        )
        messages.success(request, f"Vehículo {vehiculo.placa} asignado a {chofer.get_full_name()} correctamente.")

    return redirect('vehiculos')

def editar_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, pk=id_vehiculo)

    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Vehículo {vehiculo.placa} actualizado correctamente.")
            return redirect('vehiculos')
        else:
            messages.error(request, "Corrija los errores del formulario.")
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, 'admin/vehiculos/index.html', {
        'form': form,
        'vehiculo': vehiculo
    })