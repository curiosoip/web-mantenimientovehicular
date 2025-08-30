from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_movimientos, name='movimientos'),
    path('registrar/', views.registrar_movimiento, name='registrar_movimiento'),
    path('eliminar/<uuid:id_movimiento_repuesto>/', views.eliminar_movimiento, name='eliminar_movimiento'),
]
