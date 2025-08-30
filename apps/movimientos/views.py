from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import MovimientoRepuesto
from .forms import MovimientoForm
from apps.repuestos.models import Repuesto
from apps.vehiculos.models import Vehiculo

def index_movimientos(request):
    query = request.GET.get('q', '')
    if query:
        lista_movimientos = MovimientoRepuesto.objects.filter(
            Q(repuesto__nombre__icontains=query) |
            Q(vehiculo__placa__icontains=query) |
            Q(usuario__nombres__icontains=query) |
            Q(accion__icontains=query)
        ).order_by('-fecha')
    else:
        lista_movimientos = MovimientoRepuesto.objects.all().order_by('-fecha')

    paginacion = Paginator(lista_movimientos, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    context = {
        "banner_title": "Movimientos",
        "pagina_actual": pagina_actual,
        "vehiculos":Vehiculo.objects.all(),
        "repuestos":Repuesto.objects.all(),
        "total_registros": lista_movimientos.count(),
        "query": query
    }
    return render(request, 'admin/movimientos/index.html', context=context)

def eliminar_movimiento(request, id_movimiento_repuesto):
    movimiento = get_object_or_404(MovimientoRepuesto, id_movimiento_repuesto=id_movimiento_repuesto)
    try:
        movimiento.delete()
    except Exception as e:
        print(f"Error al eliminar el movimiento: {str(e)}")

    return redirect('movimientos')

def registrar_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movimientos')
        return redirect('movimientos')
    else:
        form = MovimientoForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Movimiento'
    }

    return render(request, 'admin/movimientos/index.html', context)
