from django.urls import path
from .views import index, eliminar_bitacora, registrar_bitacora,imprimir_bitacora

urlpatterns = [
    path('', index, name='bitacoras'),
    path('registrar/', registrar_bitacora, name='registrar_bitacora'),
    path('eliminar/<uuid:id_bitacora>/', eliminar_bitacora, name='eliminar_bitacora'),
    path('imprimir/<uuid:id_bitacora>/', imprimir_bitacora, name='imprimir_bitacora'), 

]
