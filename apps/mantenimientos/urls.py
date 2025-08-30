from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='mantenimientos'),
    path('registrar/', views.registrar_mantenimiento, name='registrar_mantenimiento'),
    path('eliminar/<uuid:id_mantenimiento>/', views.eliminar_mantenimiento, name='eliminar_mantenimiento'),
]
