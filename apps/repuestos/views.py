from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Repuesto
from .forms import RepuestoForm


def index(request):
    query = request.GET.get('q', '')
    if query:
        lista_repuestos = Repuesto.objects.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        ).order_by('nombre')
    else:
        lista_repuestos = Repuesto.objects.all().order_by('nombre')

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
        messages.success(request, "Repuesto eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el repuesto: {str(e)}")
    return redirect('repuestos')


def registrar_repuesto(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            try:
                if Repuesto.objects.filter(codigo=form.cleaned_data['codigo']).exists():
                    messages.error(request, "El código del repuesto ya existe. Elija otro.")
                    raise ValueError("Código duplicado")

                repuesto = form.save()
                messages.success(request, "Repuesto registrado correctamente.")
                return redirect('repuestos')

            except ValueError:
                return redirect('repuestos')
        else:
            for field, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{field}: {error}")
            return redirect('repuestos')
    else:
        form = RepuestoForm()

    context = {
        'form': form,
        'banner_title': 'Crear Repuesto'
    }
    return render(request, 'admin/repuestos/index.html', context)
