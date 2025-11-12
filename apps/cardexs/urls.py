from django.urls import path
from .views import index, eliminar_cardex, registrar_cardex

urlpatterns = [
    path('', index, name='cardexs'),
    path('registrar/', registrar_cardex, name='registrar_cardex'),
    path('eliminar/<uuid:id_cardex>/', eliminar_cardex, name='eliminar_cardex'),
]
