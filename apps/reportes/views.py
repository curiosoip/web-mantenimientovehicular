from django.shortcuts import render
from django.db.models import Count, Sum, Max
from django.db.models.functions import TruncDate, ExtractWeekDay
from datetime import datetime, timedelta
import json

from apps.vehiculos.models import Vehiculo
from apps.mantenimientos.models import SolicitudMantenimiento,OrdenServicio
from apps.bitacoras.models import Bitacora
from apps.consumos_combustible.models import ConsumoCombustible
from apps.repuestos.models import RepuestoUsado

def index(request):
    # 1️⃣ Mantenimientos por semana
    mantenimientos_semana = SolicitudMantenimiento.objects.annotate(
        dia_semana=ExtractWeekDay('fecha_solicitud')
    ).values('dia_semana').annotate(
        total=Count('id_solicitud_mantenimiento')
    ).order_by('dia_semana')

    labels_semana = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']  # Django: 1=Domingo
    series_semana = [0]*7
    for m in mantenimientos_semana:
        index = (m['dia_semana']-1) % 7
        series_semana[index] = m['total']

    chart_mantenimientos_semana = {
        'labels': labels_semana,
        'series': [{'name': 'Mantenimientos por Semana', 'data': series_semana}]
    }

    # 2️⃣ Consumos de combustible por semana
    consumos_semana = ConsumoCombustible.objects.annotate(
        dia_semana=ExtractWeekDay('fecha')
    ).values('dia_semana').annotate(total=Sum('litros')).order_by('dia_semana')

    series_combustible = [0]*7
    for c in consumos_semana:
        index = (c['dia_semana']-1) % 7
        series_combustible[index] = float(c['total'] or 0)

    chart_combustible_semana = {
        'labels': labels_semana,
        'series': [{'name': 'Litros por Semana', 'data': series_combustible}]
    }

    # 3️⃣ Kilometraje total por vehículo
    kilometraje = Vehiculo.objects.annotate(
        km_total=Max('bitacoras__km_final')
    ).values('placa', 'km_total').order_by('placa')

    chart_kilometraje = {
        'labels': [v['placa'] for v in kilometraje],
        'series': [{'name': 'Kilometraje Total', 'data': [v['km_total'] or 0 for v in kilometraje]}]
    }

    # 4️⃣ Cantidad de bitácoras por vehículo
    bitacoras_count = Vehiculo.objects.annotate(
        total_bitacoras=Count('bitacoras')
    ).values('placa', 'total_bitacoras').order_by('placa')

    chart_bitacoras = {
        'labels': [v['placa'] for v in bitacoras_count],
        'series': [{'name': 'Bitácoras por Vehículo', 'data': [v['total_bitacoras'] for v in bitacoras_count]}]
    }

    # 5️⃣ Órdenes de servicio por tipo de mantenimiento
    ordenes_tipo = OrdenServicio.objects.values('solicitud__tipo').annotate(
        total=Count('id_orden_servicio')
    )

    chart_ordenes_tipo = {
        'labels': [o['solicitud__tipo'] for o in ordenes_tipo],
        'series': [o['total'] for o in ordenes_tipo]
    }

    # 6️⃣ Repuestos usados por orden de servicio
    repuestos_usados = RepuestoUsado.objects.values('orden_servicio__id_orden_servicio').annotate(
        total_repuestos=Sum('cantidad')
    )

    chart_repuestos = {
        'labels': [str(r['orden_servicio__id_orden_servicio'])[:8] for r in repuestos_usados],
        'series': [r['total_repuestos'] for r in repuestos_usados]
    }

    # Serializamos todo a JSON para JS
    context = {
        'chart_mantenimientos_semana_json': json.dumps(chart_mantenimientos_semana),
        'chart_combustible_semana_json': json.dumps(chart_combustible_semana),
        'chart_kilometraje_json': json.dumps(chart_kilometraje),
        'chart_bitacoras_json': json.dumps(chart_bitacoras),
        'chart_ordenes_tipo_json': json.dumps(chart_ordenes_tipo),
        'chart_repuestos_json': json.dumps(chart_repuestos),
    }

    return render(request, 'admin/reportes/index.html', context)
