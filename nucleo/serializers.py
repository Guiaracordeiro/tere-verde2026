from rest_framework import serializers
from .models import Trilha, Avaliacao, Administrador, Evento

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['id', 'trilha', 'autor', 'comentario', 'nota', 'data']

class TrilhaSerializer(serializers.ModelSerializer):
    avaliacoes = AvaliacaoSerializer(many=True, read_only=True)

    class Meta:
        model = Trilha
        fields = [
            'id',
            'nome',
            'descricao',
            'localizacao',
            'distancia_km',
            'tempo_estimado_min',
            'dificuldade',
            'imagem_url',
            'avaliacoes',
            'criado_em'
        ]
class EventoSerializer(serializers.ModelSerializer):
    class Meta:
            model = Evento
            fields = [
            'id', 
            'titulo', 
            'data', 
            'local', 
            'descricao', 
            'criado_em'
            ]