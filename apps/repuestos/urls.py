from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='repuestos'),
    path('registrar/', views.registrar_repuesto, name='registrar_repuesto'),
    path('eliminar/<uuid:id_repuesto>/', views.eliminar_repuesto, name='eliminar_repuesto'),
]
