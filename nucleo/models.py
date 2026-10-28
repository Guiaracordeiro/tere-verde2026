from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField
from django.db import models

class Trilha(models.Model):
    DIFICULDADE_CHOICES = [
        ('FACIL', 'Fácil'),
        ('MODERADA', 'Moderada'),
        ('DIFICIL', 'Difícil'),
    ]

    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    localizacao = models.CharField(max_length=200, help_text="Bairro, parque ou ponto de referência")
    distancia_km = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    tempo_estimado_min = models.IntegerField(default=60)
    dificuldade = models.CharField(max_length=10, choices=DIFICULDADE_CHOICES, default='FACIL')
    imagem_url = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Avaliacao(models.Model):
    trilha = models.ForeignKey(Trilha, related_name='avaliacoes', on_delete=models.CASCADE)
    autor = models.CharField(max_length=100)
    comentario = models.TextField()
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor} - {self.trilha.nome} ({self.nota}/5)"
    
class Administrador(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)  # Senha com hash criptográfico
    token = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome
class Evento(models.Model):
    id = models.CharField(primary_key=True, max_length=24, default='', editable=False)
    titulo = models.CharField(max_length=150)
    data = models.CharField(max_length=50) # Ex: "15 de Novembro de 2026"
    local = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            from bson import ObjectId
            self.id = str(ObjectId())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo