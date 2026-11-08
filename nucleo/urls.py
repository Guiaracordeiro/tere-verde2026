from django.urls import path
from .views import (
    LoginView,
    EventosListCreateView,
    EventoDetailView,
    TrilhasListCreateView,
    TrilhaDetailView,
    CachoeirasListCreateView,
    CachoeiraDetailView
)

urlpatterns = [
    # Rota de Login
    path('api/login/', LoginView.as_view(), name='api-login'),

    # Rotas de Eventos
    path('api/eventos/', EventosListCreateView.as_view(), name='api-eventos'),
    path('api/eventos/<str:id>/', EventoDetailView.as_view(), name='api-evento-detail'),

    # Rotas de Trilhas
    path('api/trilhas/', TrilhasListCreateView.as_view(), name='api-trilhas'),
    path('api/trilhas/<str:id>/', TrilhaDetailView.as_view(), name='api-trilha-detail'),

    # Rotas de Cachoeiras
    path('api/cachoeiras/', CachoeirasListCreateView.as_view(), name='api-cachoeiras'),
    path('api/cachoeiras/<str:id>/', CachoeiraDetailView.as_view(), name='api-cachoeira-detail'),
]