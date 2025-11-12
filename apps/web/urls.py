
from django.urls import path,include
from .views import index,login_view,panel
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', index, name='inicio'),
    path('panel', panel, name='panel'),
    path('panel/usuarios/', include('apps.usuarios.urls')),
    path('panel/vehiculos/', include('apps.vehiculos.urls')),
    path('panel/cardexs/', include('apps.cardexs.urls')),
    path('panel/notificaciones/', include('apps.notificaciones.urls')),
    path('panel/repuestos/', include('apps.repuestos.urls')),
    path('panel/bitacoras/', include('apps.bitacoras.urls')),
    path('panel/mantenimientos/', include('apps.mantenimientos.urls')),
    path('panel/consumos-combustible/', include('apps.consumos_combustible.urls')),
    path('panel/reportes/', include('apps.reportes.urls')),
    path('login', login_view, name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    #---------analisis test
    
]
