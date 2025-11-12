from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import ConsumoCombustible
from .forms import ConsumoCombustibleForm
from apps.vehiculos.models import Vehiculo
from apps.usuarios.models import Usuario


def index(request):
    query = request.GET.get('q', '')

    # Filtrar lista de consumos según búsqueda
    if query:
        lista_consumos = ConsumoCombustible.objects.filter(
            Q(vehiculo__placa__icontains=query) |
            Q(chofer__first_name__icontains=query) |
            Q(chofer__last_name__icontains=query)
        ).order_by('-fecha')
    else:
        lista_consumos = ConsumoCombustible.objects.all().order_by('-fecha')

    # Paginación de consumos
    paginacion_consumos = Paginator(lista_consumos, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual_consumos = paginacion_consumos.get_page(numero_pagina)

    # Lista de vehículos filtrada por el departamento del usuario
    lista_vehiculos = Vehiculo.objects.filter(departamento=request.user.departamento).order_by('marca', 'modelo')

    # Lista de choferes filtrada por el departamento del usuario y rol "Chofer"
    lista_choferes = Usuario.objects.filter(
        departamento=request.user.departamento,
        rol='Chofer'
    ).order_by('first_name', 'last_name')

    context = {
        "banner_title": "Consumos de Combustible",
        "pagina_actual": pagina_actual_consumos,
        "vehiculos": lista_vehiculos,
        "choferes": lista_choferes,
        "query": query
    }

    return render(request, 'admin/consumos_combustible/index.html', context=context)


def eliminar_consumo(request, id_consumo_combustible):
    consumo = get_object_or_404(ConsumoCombustible, id_consumo_combustible=id_consumo_combustible)
    
    try:
        consumo.delete()
        messages.success(request, "Consumo eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el consumo: {str(e)}")
    
    return redirect('consumos')


def registrar_consumo(request):
    if request.method == 'POST':
        form = ConsumoCombustibleForm(request.POST)
        if form.is_valid():
            try:
                # Se guarda el consumo
                consumo = form.save(commit=False)
                consumo.save()
                messages.success(request, "Consumo registrado correctamente.")
                return redirect('consumos')
            except Exception as e:
                messages.error(request, f"Error al registrar el consumo: {str(e)}")
                return redirect('consumos')
        else:
            for field, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{field}: {error}")
            return redirect('consumos')
    else:
        form = ConsumoCombustibleForm()
    
    context = {
        'form': form,
        'banner_title': 'Registrar Consumo de Combustible'
    }
    return render(request, 'admin/consumos_combustible/index.html', context)
