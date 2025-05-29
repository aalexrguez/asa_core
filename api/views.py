from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Q
from gym.models import TipoMembresia
# Create your views here.

@api_view(['GET'])
def reporte_membresias_activas(request):
    data = TipoMembresia.objects.annotate(
        total=Count('membresia', filter=Q(membresia__mem_status=True))
    ).values('tm_nombre', 'total')

    return Response(data)

@api_view(['GET'])
def reporte_membresias_por_tipo(request):
    from gym.models import TipoMembresia
    from django.db.models import Count

    data = TipoMembresia.objects.annotate(
        cantidad=Count('membresia')
    ).values('tm_nombre', 'cantidad')

    return Response(data)
