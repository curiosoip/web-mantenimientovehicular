from django.urls import path
from .views import index, registrar_consumo, eliminar_consumo

urlpatterns = [
    path('', index, name='consumos'),
    path('registrar/', registrar_consumo, name='registrar_consumo'),
    path('eliminar/<uuid:id_consumo_combustible>/', eliminar_consumo, name='eliminar_consumo'),
]
