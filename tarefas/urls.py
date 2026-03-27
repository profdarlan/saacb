from django.urls import path
from .views import (
    TarefaListView, TarefaDetailView, TarefaCreateView, TarefaUpdateView, TarefaDeleteView,
    GerarDocumentoView, RelatorioPorUsuarioView, RelatorioConcluidasView,
    ExportCSVView, ImportCSVView, TarefaListOrdenadaView, DashboardView, DashboardDataView
)
from . import views_integracao as integracao

app_name = 'tarefas'

urlpatterns = [
    path('', TarefaListView.as_view(), name='tarefa_list'),
    path('lista/', TarefaListOrdenadaView.as_view(), name='tarefa_list_moderna'),
    path('<int:pk>/', TarefaDetailView.as_view(), name='tarefa_detail'),
    path('create/', TarefaCreateView.as_view(), name='tarefa_create'),
    path('<int:pk>/update/', TarefaUpdateView.as_view(), name='tarefa_update'),
    path('<int:pk>/delete/', TarefaDeleteView.as_view(), name='tarefa_delete'),
    path('tarefa/<int:pk>/gerar/<str:tipo>/', GerarDocumentoView.as_view(), name='gerar_documento'),
    path('relatorios/por-usuario/', RelatorioPorUsuarioView.as_view(), name='relatorio_usuario'),
    path('relatorios/concluidas/', RelatorioConcluidasView.as_view(), name='relatorio_concluidas'),
    path('export_csv/', ExportCSVView.as_view(), name='export_csv'),
    path('import_csv/', ImportCSVView.as_view(), name='import_csv'),
    
    # URLs de Integração com Planilha Cálculos
    path('tarefa/<int:tarefa_id>/calcular/', integracao.calcular_creditos_tarefa, name='integracao_calcular_creditos'),
    path('tarefa/<int:tarefa_id>/salvar-resultados/', integracao.salvar_resultados_calculo, name='integracao_salvar_resultados'),
    path('tarefa/<int:tarefa_id>/upload-pdf/', integracao.upload_pdf_tarefa, name='integracao_upload_pdf'),
    path('tarefa/<int:tarefa_id>/remover-pdf/', integracao.remover_pdf_tarefa, name='integracao_remover_pdf'),
    path('tarefa/<int:tarefa_id>/aprovar-calculos/', integracao.aprovar_calculos_tarefa, name='integracao_aprovar_calculos'),
    path('api/calcular/', integracao.calcular_ajax, name='integracao_api_calcular'),
    path('tarefa/<int:tarefa_id>/pdf/', integracao.baixar_relatorio_pdf, name='integracao_baixar_pdf'),
    path('tarefa/<int:tarefa_id>/excel/', integracao.baixar_relatorio_excel, name='integracao_baixar_excel'),
    path('api/status/', integracao.status_api, name='integracao_status_api'),
    path('tarefa/<int:tarefa_id>/aprovar-valor/', integracao.aprovar_valor, name='integracao_aprovar_valor'),
    path('tarefa/<int:tarefa_id>/gerar-salvar-pdf/', integracao.gerar_e_salvar_pdf_tarefa, name='integracao_gerar_salvar_pdf'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard-data/', DashboardDataView.as_view(), name='dashboard-data'),
]   
