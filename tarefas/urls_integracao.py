"""
URLs de Integração: SAACB ↔ Planilha Cálculos
"""
from django.urls import path
from . import views_integracao as integracao

urlpatterns = [
    # Cálculo de créditos
    path('tarefa/<int:tarefa_id>/calcular/', integracao.calcular_creditos_tarefa, name='integracao_calcular_creditos'),
    
    # API AJAX
    path('api/calcular/', integracao.calcular_ajax, name='integracao_api_calcular'),
    
    # Download de relatórios
    path('tarefa/<int:tarefa_id>/pdf/', integracao.baixar_relatorio_pdf, name='integracao_baixar_pdf'),
    path('tarefa/<int:tarefa_id>/excel/', integracao.baixar_relatorio_excel, name='integracao_baixar_excel'),
    
    # Status da API
    path('api/status/', integracao.status_api, name='integracao_status_api'),
]
