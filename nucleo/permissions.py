from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Administrador

class IsAdminOrReadOnly(BasePermission):
    """
    Permite leitura (GET, HEAD, OPTIONS) para qualquer visitante anônimo.
    Exige token de administrador válido para escrita (POST, PUT, PATCH, DELETE).
    """
    def has_permission(self, request, view):
        # Requisições de leitura são sempre liberadas
        if request.method in SAFE_METHODS:
            return True
        
        # Recupera o token enviado no cabeçalho: "Authorization: Bearer <token>"
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            return Administrador.objects.filter(token=token).exists()
        
        return False