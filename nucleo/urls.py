from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('trilhas/', views.trilhas_list_create, name='trilhas_list_create'),
    path('trilhas/<str:item_id>/', views.trilha_delete, name='trilha_delete'),
    path('cachoeiras/', views.cachoeiras_list_create, name='cachoeiras_list_create'),
    path('cachoeiras/<str:item_id>/', views.cachoeira_delete, name='cachoeira_delete'),
    path('eventos/', views.eventos_list_create, name='eventos_list_create'),
    path('eventos/<str:item_id>/', views.evento_delete, name='evento_delete'),
]