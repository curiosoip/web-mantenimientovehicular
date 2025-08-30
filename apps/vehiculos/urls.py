
from django.urls import path
from .views import index,eliminar_vehiculo,registrar_vehiculo

urlpatterns = [
    path('', index, name='vehiculos'),
    path('registrar/', registrar_vehiculo, name='registrar_vehiculo'),
    path('eliminar/<uuid:id_vehiculo>/', eliminar_vehiculo, name='eliminar_vehiculo'),
]
