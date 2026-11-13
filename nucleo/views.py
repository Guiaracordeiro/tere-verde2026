import os
import uuid
import certifi
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

load_dotenv()

# Conexão segura com MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "123456")
ADMIN_TOKEN = "token_tere_verde_admin_2026"

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["tere_verde_db"]

col_trilhas = db["trilhas"]
col_cachoeiras = db["cachoeiras"]
col_eventos = db["eventos"]


def verificar_token(request):
    """Valida o cabeçalho Authorization: Bearer <token>."""
    auth = request.headers.get("Authorization", "")
    return auth == f"Bearer {ADMIN_TOKEN}"


def salvar_imagem_upload(request):
    """Salva a foto enviada no campo 'imagem' e devolve a URL pública."""
    arquivo = request.FILES.get("imagem")
    if not arquivo:
        return ""
    extensao = arquivo.name.split(".")[-1]
    nome_unico = f"uploads/{uuid.uuid4().hex}.{extensao}"
    caminho_salvo = default_storage.save(nome_unico, ContentFile(arquivo.read()))
    return f"http://127.0.0.1:8000/media/{caminho_salvo}"


def serializar_doc(doc):
    """Converte o _id do MongoDB para string 'id'."""
    doc["id"] = str(doc.pop("_id"))
    return doc


# ================= LOGIN ADMINISTRATIVO =================
@api_view(["POST"])
def admin_login(request):
    usuario = request.data.get("usuario") or request.data.get("username")
    senha = request.data.get("senha") or request.data.get("password")

    if usuario == ADMIN_USER and senha == ADMIN_PASSWORD:
        return Response({"token": ADMIN_TOKEN, "mensagem": "Login realizado com sucesso!"})
    return Response({"erro": "Usuário ou senha inválidos."}, status=status.HTTP_401_UNAUTHORIZED)


# ================= TRILHAS =================
@api_view(["GET", "POST"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def trilhas_list_create(request):
    if request.method == "GET":
        trilhas = [serializar_doc(t) for t in col_trilhas.find()]
        return Response(trilhas)

    if not verificar_token(request):
        return Response({"erro": "Não autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    imagem_url = salvar_imagem_upload(request)
    novo_doc = {
        "nome": request.data.get("nome", ""),
        "parque": request.data.get("parque", ""),
        "dificuldade": request.data.get("dificuldade", ""),
        "distancia": request.data.get("distancia", ""),
        "tempo": request.data.get("tempo", ""),
        "altitude": request.data.get("altitude", ""),
        "descricao": request.data.get("descricao", ""),
        "imagem_url": imagem_url,
    }
    res = col_trilhas.insert_one(novo_doc)
    novo_doc["id"] = str(res.inserted_id)
    novo_doc.pop("_id", None)
    return Response(novo_doc, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def trilha_delete(request, item_id):
    if not verificar_token(request):
        return Response({"erro": "Não autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
    col_trilhas.delete_one({"_id": ObjectId(item_id)})
    return Response(status=status.HTTP_204_NO_CONTENT)


# ================= CACHOEIRAS =================
@api_view(["GET", "POST"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def cachoeiras_list_create(request):
    if request.method == "GET":
        cachoeiras = [serializar_doc(c) for c in col_cachoeiras.find()]
        return Response(cachoeiras)

    if not verificar_token(request):
        return Response({"erro": "Não autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    imagem_url = salvar_imagem_upload(request)
    banho_raw = str(request.data.get("propria_banho", "")).lower()
    propria_banho = banho_raw in ["true", "1", "sim", "on"]

    novo_doc = {
        "nome": request.data.get("nome", ""),
        "parque": request.data.get("parque", ""),
        "acesso": request.data.get("acesso", ""),
        "propria_banho": propria_banho,
        "descricao": request.data.get("descricao", ""),
        "imagem_url": imagem_url,
    }
    res = col_cachoeiras.insert_one(novo_doc)
    novo_doc["id"] = str(res.inserted_id)
    novo_doc.pop("_id", None)
    return Response(novo_doc, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def cachoeira_delete(request, item_id):
    if not verificar_token(request):
        return Response({"erro": "Não autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
    col_cachoeiras.delete_one({"_id": ObjectId(item_id)})
    return Response(status=status.HTTP_204_NO_CONTENT)


# ================= EVENTOS =================
@api_view(["GET", "POST"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def eventos_list_create(request):
    if request.method == "GET":
        eventos = [serializar_doc(e) for e in col_eventos.find()]
        return Response(eventos)

    if not verificar_token(request):
        return Response({"erro": "Não autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    imagem_url = salvar_imagem_upload(request)
    novo_doc = {
        "titulo": request.data.get("titulo", ""),
        "parque": request.data.get("parque", ""),
        "data_evento": request.data.get("data_evento", ""),
        "horario": request.data.get("horario", ""),
        "local": request.data.get("local", ""),
        "descricao": request.data.get("descricao", ""),
        "imagem_url": imagem_url,
    }
    res = col_eventos.insert_one(novo_doc)
    novo_doc["id"] = str(res.inserted_id)
    novo_doc.pop("_id", None)
    return Response(novo_doc, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def evento_delete(request, item_id):
    if not verificar_token(request):
        return Response({"erro": "Não autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
    col_eventos.delete_one({"_id": ObjectId(item_id)})
    return Response(status=status.HTTP_204_NO_CONTENT)