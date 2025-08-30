
from django.urls import path,include
from .views import index,login_view,panel
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', index, name='inicio'),
    path('panel', panel, name='panel'),
    path('panel/usuarios/', include('apps.usuarios.urls')),
    path('panel/vehiculos/', include('apps.vehiculos.urls')),
    path('panel/repuestos/', include('apps.repuestos.urls')),
    path('panel/bitacoras/', include('apps.bitacoras.urls')),
    path('panel/mantenimientos/', include('apps.mantenimientos.urls')),
    path('panel/movimientos/', include('apps.movimientos.urls')),
    path('panel/reportes/', include('apps.reportes.urls')),
    path('login', login_view, name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    #---------analisis test
    path('analisis/', include('apps.analisis.urls')),
    
]
