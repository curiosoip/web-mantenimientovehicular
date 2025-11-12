from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Bitacora
from .forms import BitacoraForm  
from apps.vehiculos.models import Vehiculo
from apps.usuarios.models import Usuario

def index(request):
    query = request.GET.get('q', '')
    user = request.user

    form = BitacoraForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Bitácora registrada correctamente.")
        return redirect('bitacoras')
    elif request.method == 'POST':
        for field, errores in form.errors.items():
            for error in errores:
                messages.error(request, f"{field}: {error}")
        return redirect('bitacoras')

    if query:
        lista_bitacoras = Bitacora.objects.filter(
            Q(vehiculo__placa__icontains=query) |
            Q(chofer__first_name__icontains=query) |
            Q(chofer__last_name__icontains=query) |
            Q(observaciones__icontains=query)
        ).order_by('-fecha')
    else:
        lista_bitacoras = Bitacora.objects.all().order_by('-fecha')

    if user.is_superuser:
        vehiculos = Vehiculo.objects.all().order_by('placa')
        choferes = Usuario.objects.filter(rol='Chofer').order_by('first_name')
    else:
        vehiculos = Vehiculo.objects.filter(departamento=user.departamento).order_by('placa')
        choferes = Usuario.objects.filter(rol='Chofer', departamento=user.departamento).order_by('first_name')

    paginacion = Paginator(lista_bitacoras, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    context = {
        "banner_title": "Bitácoras",
        "pagina_actual": pagina_actual,
        "total_registros": lista_bitacoras.count(),
        "query": query,
        "vehiculos": vehiculos,
        "choferes": choferes,
        "form": form  
    }
    return render(request, 'admin/bitacoras/index.html', context=context)



def eliminar_bitacora(request, id_bitacora):
    bitacora = get_object_or_404(Bitacora, id_bitacora=id_bitacora)
    try:
        bitacora.delete()
        messages.success(request, "Bitácora eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la bitácora: {str(e)}")
    return redirect('bitacoras')

def imprimir_bitacora(request, id_bitacora):
    bitacora = get_object_or_404(Bitacora, id_bitacora=id_bitacora)
    context = {
        "bitacora": bitacora
    }
    return render(request, "admin/bitacoras/bitacora_pdf.html", context)


def registrar_bitacora(request):
    if request.method == 'POST':
        form = BitacoraForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Bitácora registrada correctamente.")
            return redirect('bitacoras')
        else:
            # Mostrar errores del formulario
            for field, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{field}: {error}")
            return redirect('bitacoras')  # redirige para que se vean los mensajes

    return redirect('bitacoras')

