from django.urls import path
from .views import index, eliminar_repuesto, registrar_repuesto

urlpatterns = [
    path('', index, name='repuestos'),
    path('registrar/', registrar_repuesto, name='registrar_repuesto'),
    path('eliminar/<uuid:id_repuesto>/', eliminar_repuesto, name='eliminar_repuesto'),
]
