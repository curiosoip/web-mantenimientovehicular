from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'login.html')

def panel(request):
    return render(request, 'admin/_base.html')



def login_view(request):
    if request.user.is_authenticated:
        if request.user.rol == 'Administrador general':
            return redirect('vehiculos')
        elif request.user.rol == 'Jefe de unidad':
            return redirect('vehiculos')
        elif request.user.rol == 'Encargado parque motor':
            return redirect('vehiculos')
        elif request.user.rol == 'Chofer':
            return redirect('vehiculos')
        elif request.user.rol == 'Finanzas':
            return redirect('vehiculos')
        else:
            return redirect('login') 

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.rol == 'Administrador general':
                return redirect('vehiculos')
            elif request.user.rol == 'Jefe de unidad':
                return redirect('vehiculos')
            elif request.user.rol == 'Encargado parque motor':
                return redirect('vehiculos')
            elif request.user.rol == 'Chofer':
                return redirect('vehiculos')
            elif request.user.rol == 'Finanzas':
                return redirect('vehiculos')
            else:
                return redirect('login')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

