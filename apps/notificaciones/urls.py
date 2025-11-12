from django.urls import path
from .views import index, eliminarnotificacion, registrar_notificacion,marcar_leida

urlpatterns = [
    path('', index, name='notificaciones'),  
    path('registrar/', registrar_notificacion, name='registrar_notificacion'), 
    path('marcar-leida/<uuid:id_notificacion>/', marcar_leida, name='marcar_leida'),
    path('eliminar/<uuid:id_notificacion>/', eliminarnotificacion, name='eliminar_notificacion'),  
]
