
from django.urls import path
from .views import index,eliminar_vehiculo,registrar_vehiculo,editar_vehiculo,cambiar_estado_vehiculo,asignar_vehiculo

urlpatterns = [
    path('', index, name='vehiculos'),
    path('registrar/', registrar_vehiculo, name='registrar_vehiculo'),
    path('eliminar/<uuid:id_vehiculo>/', eliminar_vehiculo, name='eliminar_vehiculo'),
    path('cambiar-estado/<uuid:id_vehiculo>/', cambiar_estado_vehiculo, name='cambiar_estado_vehiculo'),
    path('asignar/<uuid:id_vehiculo>/', asignar_vehiculo, name='asignar_vehiculo'),
    path('editar/<uuid:id_vehiculo>/', editar_vehiculo, name='editar_vehiculo'),
]
