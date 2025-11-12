from django.shortcuts import render
from .models import Usuario
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from .forms import UsuarioForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages


def index(request):
    query = request.GET.get('q','') 
    if query:
        lista_usuarios = Usuario.objects.filter(
            Q(first_name__icontains=query) |  
            Q(last_name__icontains=query) |
            Q(username__icontains=query) 
        ).order_by('-fecha_registro')  
    else:
        lista_usuarios = Usuario.objects.all().order_by('-fecha_registro')  
    paginacion=Paginator(lista_usuarios,6)
    numero_pagina=request.GET.get('page')
    pagina_actual=paginacion.get_page(numero_pagina)
    context={
        "banner_title":"Usuarios",
        "pagina_actual":pagina_actual,
        "total_registros": lista_usuarios.count(),
        "query": query
        
    }
    return render(request, 'admin/usuarios/index.html',context=context)

def eliminarusuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    try:
        usuario.delete()
    except Exception as e:
        print(f"Error al eliminar el usuario: {str(e)}")
    
    return redirect('usuarios')

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                if Usuario.objects.filter(username=form.cleaned_data['username']).exists():
                    messages.error(request, "El nombre de usuario ya existe. Elija otro.")
                    raise ValueError("Username duplicado")

                if Usuario.objects.filter(email=form.cleaned_data['email']).exists():
                    messages.error(request, "El correo electrónico ya está registrado. Use otro.")
                    raise ValueError("Email duplicado")

                usuario = form.save(commit=False)
                usuario.password = make_password(form.cleaned_data['password'])
                usuario.save()
                messages.success(request, "Usuario registrado correctamente.")
                return redirect('usuarios')

            except ValueError:
                return redirect('usuarios')
        else:
            for field, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{field}: {error}")
            return redirect('usuarios')
    else:
        form = UsuarioForm()

    context = {
        'form': form,
        'banner_title': 'Crear Usuario'
    }
    return render(request, 'admin/usuarios/index.html', context)