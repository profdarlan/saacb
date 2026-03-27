"""
URLs para o prefixo /api/ — usadas em produção quando API_BASE = '/api'.

Em desenvolvimento, o browser chama a API FastAPI diretamente (outro host/porta).
Em produção (saacb.lakeserver.online), API_BASE = '/api' aponta para estas views
Django, que fazem as chamadas server-to-server para a API FastAPI (sem CORS).
"""
from django.urls import path
from . import views_integracao as integracao

urlpatterns = [
    path('status', integracao.api_proxy_status, name='api_proxy_status'),
    path('indices-padrao', integracao.api_proxy_indices_padrao, name='api_proxy_indices_padrao'),
    path('upload-pdf', integracao.api_proxy_upload_pdf, name='api_proxy_upload_pdf'),
    path('gerar-relatorio-pdf', integracao.api_proxy_gerar_pdf, name='api_proxy_gerar_pdf'),
    path('gerar-excel', integracao.api_proxy_gerar_excel, name='api_proxy_gerar_excel'),
]
