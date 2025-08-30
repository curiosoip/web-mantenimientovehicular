# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BitacoraViaje
from .forms import BitacoraForm
from apps.vehiculos.models import Vehiculo
from django.contrib.auth.decorators import login_required

@login_required
def index_bitacoras(request):
    query = request.GET.get('q', '')
    if query:
        lista_bitacoras = BitacoraViaje.objects.filter(
            Q(vehiculo__placa__icontains=query) |
            Q(ruta__icontains=query) |
            Q(observaciones__icontains=query)
        ).order_by('-fecha')
    else:
        lista_bitacoras = BitacoraViaje.objects.all().order_by('-fecha')

    paginacion = Paginator(lista_bitacoras, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    context = {
        "banner_title": "Bitácoras de Viaje",
        "pagina_actual": pagina_actual,
        "vehiculos": Vehiculo.objects.all(),
        "total_registros": lista_bitacoras.count(),
        "query": query
    }
    return render(request, 'admin/bitacoras/index.html', context)

@login_required
def eliminar_bitacora(request, id_bitacora_viaje):
    bitacora = get_object_or_404(BitacoraViaje, id_bitacora_viaje=id_bitacora_viaje)
    try:
        bitacora.delete()
    except Exception as e:
        print(f"Error al eliminar la bitácora: {str(e)}")
    return redirect('bitacoras')

@login_required
def registrar_bitacora(request):
    if request.method == 'POST':
        form = BitacoraForm(request.POST)
        if form.is_valid():
            bitacora = form.save(commit=False)
            bitacora.conductor = request.user  # asigna automáticamente al usuario actual
            bitacora.save()
            return redirect('bitacoras')
        return redirect('bitacoras')
    else:
        form = BitacoraForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Bitácora'
    }

    return render(request, 'admin/bitacoras/index.html', context)
