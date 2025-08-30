from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Repuesto
from .forms import RepuestoForm

def index(request):
    query = request.GET.get('q', '')
    if query:
        lista_repuestos = Repuesto.objects.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        ).order_by('-fecha_registro')
    else:
        lista_repuestos = Repuesto.objects.all().order_by('-fecha_registro')

    paginacion = Paginator(lista_repuestos, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    context = {
        "banner_title": "Repuestos",
        "pagina_actual": pagina_actual,
        "total_registros": lista_repuestos.count(),
        "query": query
    }
    return render(request, 'admin/repuestos/index.html', context=context)

def eliminar_repuesto(request, id_repuesto):
    repuesto = get_object_or_404(Repuesto, id_repuesto=id_repuesto)
    try:
        repuesto.delete()
    except Exception as e:
        print(f"Error al eliminar el repuesto: {str(e)}")

    return redirect('repuestos')

def registrar_repuesto(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('repuestos')
        return redirect('repuestos')
    else:
        form = RepuestoForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Repuesto'
    }

    return render(request, 'admin/repuestos/index.html', context)
