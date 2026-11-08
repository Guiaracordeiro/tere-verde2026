import os
import certifi
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, AllowAny

# ==============================================================================
# CARREGAMENTO DE VARIÁVEIS DE AMBIENTE (.env)
# ==============================================================================
load_dotenv()

# ==============================================================================
# CONFIGURAÇÃO DE PERSISTÊNCIA - MONGODB ATLAS (RNF04)
# ==============================================================================
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print(">>> AVISO: Variável MONGO_URI não encontrada no arquivo .env! <<<")

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)
db = client["tere_verde_db"]

col_eventos = db["eventos"]
col_trilhas = db["trilhas"]
col_cachoeiras = db["cachoeiras"]

TOKEN_ADMIN_VALIDO = "token-autenticacao-admin-tere-verde-2026"

# Helper para converter ObjectId do MongoDB em String JSON
def serialize_doc(doc):
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

# ==============================================================================
# CONTROLE DE ACESSO E SEGURANÇA (RNF03)
# ==============================================================================
class IsAdminTokenValid(BasePermission):
    """
    Permite leitura (GET) pública para qualquer visitante.
    Exige cabeçalho 'Authorization: Bearer <token>' para POST, PUT e DELETE.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            return token == TOKEN_ADMIN_VALIDO
        return False

# ==============================================================================
# LOGIN ADMINISTRATIVO (Lê credenciais do .env para evitar alerta do navegador)
# ==============================================================================
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Lê do .env ou usa valores seguros como fallback
        expected_user = os.getenv("ADMIN_USER", "admin_tere")
        expected_pass = os.getenv("ADMIN_PASSWORD", "TereVerde2026")

        if username == expected_user and password == expected_pass:
            return Response({"token": TOKEN_ADMIN_VALIDO}, status=status.HTTP_200_OK)

        return Response(
            {"erro": "Usuário ou senha incorretos."},
            status=status.HTTP_401_UNAUTHORIZED
        )

# ==============================================================================
# CRUD - EVENTOS
# ==============================================================================
class EventosListCreateView(APIView):
    permission_classes = [IsAdminTokenValid]

    def get(self, request):
        eventos = [serialize_doc(doc) for doc in col_eventos.find()]
        return Response(eventos, status=status.HTTP_200_OK)

    def post(self, request):
        dados = request.data.copy()
        if not dados.get("titulo") or not dados.get("data_evento"):
            return Response({"erro": "Campos obrigatórios ausentes."}, status=status.HTTP_400_BAD_REQUEST)
        
        resultado = col_eventos.insert_one(dados)
        dados["id"] = str(resultado.inserted_id)
        if "_id" in dados:
            del dados["_id"]
        return Response(dados, status=status.HTTP_201_CREATED)

class EventoDetailView(APIView):
    permission_classes = [IsAdminTokenValid]

    def get(self, request, id):
        try:
            doc = col_eventos.find_one({"_id": ObjectId(id)})
            if not doc:
                return Response({"erro": "Evento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
            return Response(serialize_doc(doc), status=status.HTTP_200_OK)
        except Exception:
            return Response({"erro": "ID inválido."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            dados = request.data.copy()
            if "_id" in dados:
                del dados["_id"]
            if "id" in dados:
                del dados["id"]
                
            res = col_eventos.update_one({"_id": ObjectId(id)}, {"$set": dados})
            if res.matched_count == 0:
                return Response({"erro": "Evento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
            dados["id"] = id
            return Response(dados, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            res = col_eventos.delete_one({"_id": ObjectId(id)})
            if res.deleted_count == 0:
                return Response({"erro": "Evento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"mensagem": "Evento removido com sucesso."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"erro": "ID inválido."}, status=status.HTTP_400_BAD_REQUEST)

# ==============================================================================
# CRUD - TRILHAS
# ==============================================================================
class TrilhasListCreateView(APIView):
    permission_classes = [IsAdminTokenValid]

    def get(self, request):
        trilhas = [serialize_doc(doc) for doc in col_trilhas.find()]
        return Response(trilhas, status=status.HTTP_200_OK)

    def post(self, request):
        dados = request.data.copy()
        if not dados.get("nome") or not dados.get("parque"):
            return Response({"erro": "Campos obrigatórios ausentes."}, status=status.HTTP_400_BAD_REQUEST)
        
        resultado = col_trilhas.insert_one(dados)
        dados["id"] = str(resultado.inserted_id)
        if "_id" in dados:
            del dados["_id"]
        return Response(dados, status=status.HTTP_201_CREATED)

class TrilhaDetailView(APIView):
    permission_classes = [IsAdminTokenValid]

    def delete(self, request, id):
        try:
            res = col_trilhas.delete_one({"_id": ObjectId(id)})
            if res.deleted_count == 0:
                return Response({"erro": "Trilha não encontrada."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"mensagem": "Trilha removida com sucesso."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"erro": "ID inválido."}, status=status.HTTP_400_BAD_REQUEST)

# ==============================================================================
# CRUD - CACHOEIRAS
# ==============================================================================
class CachoeirasListCreateView(APIView):
    permission_classes = [IsAdminTokenValid]

    def get(self, request):
        cachoeiras = [serialize_doc(doc) for doc in col_cachoeiras.find()]
        return Response(cachoeiras, status=status.HTTP_200_OK)

    def post(self, request):
        dados = request.data.copy()
        if not dados.get("nome") or not dados.get("parque"):
            return Response({"erro": "Campos obrigatórios ausentes."}, status=status.HTTP_400_BAD_REQUEST)
        
        resultado = col_cachoeiras.insert_one(dados)
        dados["id"] = str(resultado.inserted_id)
        if "_id" in dados:
            del dados["_id"]
        return Response(dados, status=status.HTTP_201_CREATED)

class CachoeiraDetailView(APIView):
    permission_classes = [IsAdminTokenValid]

    def delete(self, request, id):
        try:
            res = col_cachoeiras.delete_one({"_id": ObjectId(id)})
            if res.deleted_count == 0:
                return Response({"erro": "Cachoeira não encontrada."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"mensagem": "Cachoeira removida com sucesso."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"erro": "ID inválido."}, status=status.HTTP_400_BAD_REQUEST)