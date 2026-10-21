from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrilhaViewSet, AvaliacaoViewSet

router = DefaultRouter()
router.register(r'trilhas', TrilhaViewSet, basename='trilha')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacao')

urlpatterns = [
    path('', include(router.urls)),
]