from rest_framework import viewsets, filters
from .models import Trilha, Avaliacao
from .serializers import TrilhaSerializer, AvaliacaoSerializer

class TrilhaViewSet(viewsets.ModelViewSet):
    queryset = Trilha.objects.all().order_by('-criado_em')
    serializer_class = TrilhaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'localizacao', 'dificuldade']

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all().order_by('-data')
    serializer_class = AvaliacaoSerializer