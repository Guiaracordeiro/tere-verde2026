from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrilhaViewSet, AvaliacaoViewSet, LoginAdminView, EventoViewSet

router = DefaultRouter()
router.register(r'trilhas', TrilhaViewSet, basename='trilha')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacao')
router.register(r'eventos', EventoViewSet, basename='evento')
urlpatterns = [
    path('login/', LoginAdminView.as_view(), name='admin-login'),
    path('', include(router.urls)),
]
