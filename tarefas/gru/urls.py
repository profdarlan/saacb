"""
🔗 URLS PARA MÓDULO GRU
tarefas/gru/urls.py - Adicione ao seu projeto
"""

from django.urls import path
from . import views

app_name = 'gru'

urlpatterns = [
    # Home do módulo GRU
    path('', views.gru_home, name='home'),
    
    # Consultar GRU
    path('consultar/', views.ConsultarGRUView.as_view(), name='consultar'),
    
    # Histórico de consultas
    path('historico/', views.HistoricoGRUView.as_view(), name='historico'),
    
    # Estatísticas
    path('estatisticas/', views.EstatisticasGRUView.as_view(), name='estatisticas'),
    
    # Download de PDF
    path('download/<str:arquivo>/', views.DownloadGRUPDFView.as_view(), name='download_pdf'),
    
    # Listagem simples / histórico (alias 'list' usado pela UI)
    path('list/', views.HistoricoGRUView.as_view(), name='list'),
    
    # Criar/gerar GRU manualmente a partir do formulário (POST)
    path('create/', views.CriarGRUView.as_view(), name='create'),
    # ========== APIs AJAX ==========
    
    # Validar número de GRU
    path('api/validar/', views.ValidarGRUAPIView.as_view(), name='api_validar'),
    
    # Verificar disponibilidade da API
    path('api/disponibilidade/', views.DisponibilidadeAPIView.as_view(), name='api_disponibilidade'),
    
    # Informações sobre API SISGRU
    path('api/info/', views.gru_api_info, name='api_info'),
]

# ========== HANDLERS DE ERRO ==========
# Adicione ao urls.py PRINCIPAL (projeto_saacb/urls.py):
# handler404 = 'tarefas.gru.views.error_404'
# handler500 = 'tarefas.gru.views.error_500'
