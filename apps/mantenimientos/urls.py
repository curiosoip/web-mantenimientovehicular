from django.urls import path
from .views import (
    index,
    registrar_solicitud,
    eliminar_solicitud,
    detalle_solicitud  
)

urlpatterns = [
    path('solicitudes/', index, name='solicitudes'),
    path('solicitudes/registrar/', registrar_solicitud, name='registrar_solicitud'),
    path('solicitudes/eliminar/<uuid:id_solicitud>/', eliminar_solicitud, name='eliminar_solicitud'),
    path('solicitudes/detalle/<uuid:id_solicitud>/', detalle_solicitud, name='detalle_solicitud'),  # opcional
]
