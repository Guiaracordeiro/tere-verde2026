import secrets
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Trilha, Avaliacao, Administrador, Evento
from .serializers import TrilhaSerializer, AvaliacaoSerializer, EventoSerializer
from .permissions import IsAdminOrReadOnly

class TrilhaViewSet(viewsets.ModelViewSet):
    """CRUD de Trilhas: leitura livre, escrita restrita ao administrador."""
    queryset = Trilha.objects.all()
    serializer_class = TrilhaSerializer
    permission_classes = [IsAdminOrReadOnly]

class AvaliacaoViewSet(viewsets.ModelViewSet):
    """CRUD de Avaliações: leitura livre, escrita restrita ao administrador."""
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [IsAdminOrReadOnly]

class LoginAdminView(APIView):
    """Endpoint para autenticar o administrador e retornar o token de sessão."""
    
    def get(self, request):
        return Response({
            "instrucao": "Envie uma requisicao POST com 'email' e 'senha' para obter o token de acesso."
        }, status=status.HTTP_200_OK)

    def post(self, request):
        email = request.data.get('email', '').strip()
        senha = request.data.get('senha', '').strip()

        if not email or not senha:
            return Response(
                {"erro": "Email e senha são obrigatórios."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Busca pelo primeiro registro para evitar erro de duplicidade
        admin = Administrador.objects.filter(email=email).first()

        if admin and check_password(senha, admin.senha):
            novo_token = secrets.token_hex(24)
            admin.token = novo_token
            admin.save()
            return Response({
                "mensagem": "Login realizado com sucesso!",
                "token": novo_token,
                "admin": admin.nome
            }, status=status.HTTP_200_OK)
        
        return Response(
            {"erro": "Credenciais inválidas."}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class EventoViewSet(viewsets.ModelViewSet):
    """CRUD de Eventos: leitura pública, criação/edição/exclusão apenas para Admin com Token."""
    queryset = Evento.objects.all().order_by('-criado_em')
    serializer_class = EventoSerializer
    permission_classes = [IsAdminOrReadOnly]    