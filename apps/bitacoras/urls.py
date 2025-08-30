# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_bitacoras, name='bitacoras'),
    path('registrar/', views.registrar_bitacora, name='registrar_bitacora'),
    path('eliminar/<uuid:id_bitacora_viaje>/', views.eliminar_bitacora, name='eliminar_bitacora'),
]
