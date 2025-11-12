from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Cardex
from apps.vehiculos.models import Vehiculo

from .forms import CardexForm



def index(request):
    query = request.GET.get('q', '')

    # Filtrado de cardex
    if query:
        lista_cardex = Cardex.objects.filter(
            Q(vehiculo__placa__icontains=query) |
            Q(vehiculo__marca__icontains=query) |
            Q(vehiculo__modelo__icontains=query)
        ).order_by('-fecha_registro')
    else:
        lista_cardex = Cardex.objects.all().order_by('-fecha_registro')

    # Paginación
    paginacion = Paginator(lista_cardex, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    # Lista de vehículos (para selects o formularios)
    lista_vehiculos = Vehiculo.objects.all().order_by('placa')

    context = {
        "banner_title": "Cardex Vehiculares",
        "pagina_actual": pagina_actual,
        "total_registros": lista_cardex.count(),
        "query": query,
        "vehiculos": lista_vehiculos,  # <-- añadida
    }
    return render(request, 'admin/cardexs/index.html', context=context)


def eliminar_cardex(request, id_cardex):
    cardex = get_object_or_404(Cardex, id_cardex=id_cardex)
    try:
        cardex.delete()
        messages.success(request, "Cardex eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar el cardex: {str(e)}")
        messages.error(request, "Ocurrió un error al eliminar el cardex.")
    
    return redirect('cardexs')


def registrar_cardex(request):
    if request.method == 'POST':
        form = CardexForm(request.POST)

        if form.is_valid():
            vehiculo = form.cleaned_data.get('vehiculo')

            if Cardex.objects.filter(vehiculo=vehiculo).exists():
                messages.error(request, f"El vehículo {vehiculo.placa} ya tiene un Cardex registrado. Elija otro vehículo.")
            else:
                form.save()
                messages.success(request, f"Cardex para {vehiculo.placa} registrado correctamente.")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return redirect('cardexs')
