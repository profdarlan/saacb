"""
👁️ VIEWS PARA GERENCIAMENTO DE GRU
tarefas/gru/views.py - Adicione ao seu projeto
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, FileResponse, HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
import os
import logging
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .gru_service import SISGRUService, GRUPDFGenerator, SISGRUAPIError
from .forms import ConsultarGRUForm, GerarGRUForm, FiltroGRUForm
from decimal import Decimal
from tarefas.models import GRU
from .forms import GRUModelForm
from django.conf import settings

logger = logging.getLogger(__name__)

@login_required
def gru_home(request):
    """
    View principal do módulo GRU
    Dashboard com estatísticas e informações sobre GRUs
    """

    # TODO: Quando tiver o modelo GRU, buscar estatísticas reais do banco
    # from .models import GRU
    # stats = {
    #     'pendentes': GRU.objects.filter(status='PENDENTE').count(),
    #     'pagas': GRU.objects.filter(status='PAGA').count(),
    #     'vencidas': GRU.objects.filter(status='VENCIDA').count(),
    #     'total_grus': GRU.objects.count(),
    # }

    # Por enquanto, estatísticas mockadas
    stats = {
        'pendentes': 0,
        'pagas': 0,
        'vencidas': 0,
        'total_grus': 0,
    }

    context = {
        'stats': stats,
    }

    return render(request, 'gru/home.html', context)

class ConsultarGRUView(LoginRequiredMixin, View):
    """
    View para consultar uma GRU na API SISGRU.
    
    ✅ Funcionalidades:
    - Formulário com validações
    - Integração com API SISGRU
    - Geração de PDF
    - Histórico de consultas
    - Tratamento de erros
    
    📍 URL: /gru/consultar/
    """
    
    template_name = 'gru/consultar.html'
    
    def get(self, request):
        """Exibir formulário de consulta"""
        form = ConsultarGRUForm()
        
        # Carregar consultas anteriores do usuário
        consultas_recentes = self._get_consultas_recentes(request)
        
        return render(request, self.template_name, {
            'form': form,
            'consultas_recentes': consultas_recentes,
            'titulo': 'Consultar GRU',
            'descricao': 'Consulte informações sobre uma Guia de Recolhimento da União'
        })
    
    def post(self, request):
        """Processar consulta de GRU"""
        form = ConsultarGRUForm(request.POST)
        
        if form.is_valid():
            try:
                # Extrair dados do formulário
                numero_gru = form.cleaned_data['numero_gru']
                usuario = form.cleaned_data['usuario_sisgru']
                senha = form.cleaned_data['senha_sisgru']
                usar_producao = form.cleaned_data['usar_producao']
                gerar_pdf = form.cleaned_data['gerar_pdf']
                
                logger.info(f"Consultando GRU {numero_gru} - Usuário: {usuario}")
                
                # Inicializar serviço
                service = SISGRUService(
                    usuario=usuario,
                    senha=senha,
                    producao=usar_producao
                )
                
                # Consultar GRU
                resultado = service.consultar_gru(numero_gru)
                
                # Extrair dados
                dados = service.extrair_dados_gru(resultado)
                
                # Gerar PDF se solicitado
                pdf_url = None
                if gerar_pdf:
                    try:
                        generator = GRUPDFGenerator()
                        
                        # Criar diretório de PDFs se não existir
                        pdf_dir = 'media/gru_pdfs'
                        os.makedirs(pdf_dir, exist_ok=True)
                        
                        # Gerar nome único para arquivo
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        arquivo_nome = f"gru_{numero_gru}_{timestamp}.pdf"
                        arquivo_path = os.path.join(pdf_dir, arquivo_nome)
                        
                        # Gerar PDF
                        generator.gerar_pdf(dados, arquivo_path)
                        
                        # URL para download
                        pdf_url = f"/media/gru_pdfs/{arquivo_nome}"
                        
                        messages.success(request, f'✓ PDF gerado com sucesso')
                        
                    except Exception as e:
                        logger.error(f"Erro ao gerar PDF: {str(e)}")
                        messages.warning(request, f'⚠️ PDF não pôde ser gerado: {str(e)}')
                
                # Salvar consulta no histórico (opcional - se implementar modelo)
                self._salvar_historico(request, numero_gru, 'sucesso')
                
                messages.success(request, f'✓ GRU consultada com sucesso')
                
                return render(request, 'gru/resultado.html', {
                    'dados': dados,
                    'pdf_url': pdf_url,
                    'sucesso': True,
                    'numero_gru_formatado': self._formatar_numero(numero_gru)
                })
                
            except SISGRUAPIError as e:
                logger.error(f"Erro API SISGRU: {str(e)}")
                self._salvar_historico(request, 
                                      form.cleaned_data.get('numero_gru'), 
                                      'erro', str(e))
                messages.error(request, f'❌ Erro: {str(e)}')
                
                return render(request, self.template_name, {
                    'form': form,
                    'erro': str(e),
                    'sucesso': False
                })
                
            except Exception as e:
                logger.exception(f"Erro inesperado: {str(e)}")
                messages.error(request, f'❌ Erro inesperado: {str(e)}')
                
                return render(request, self.template_name, {
                    'form': form,
                    'erro': 'Erro inesperado. Tente novamente.',
                    'sucesso': False
                })
        
        return render(request, self.template_name, {'form': form})
    
    def _get_consultas_recentes(self, request, limite=5):
        """Obter consultas recentes do usuário (usar cache/BD se implementar)"""
        # TODO: Implementar se criar modelo GRU
        return []
    
    def _salvar_historico(self, request, numero_gru, status, erro=None):
        """Salvar consulta no histórico"""
        # TODO: Implementar se criar modelo ConsultaGRU
        logger.info(f"Consulta: {numero_gru} - Status: {status}")
    
    def _formatar_numero(self, numero):
        """Formata número de GRU para exibição"""
        if len(numero) != 32:
            return numero
        
        partes = [
            numero[0:4],
            numero[4:8],
            numero[8:12],
            numero[12:16],
            numero[16:20],
            numero[20:24],
            numero[24:28],
            numero[28:32],
        ]
        
        return ".".join(partes)


class DownloadGRUPDFView(LoginRequiredMixin, View):
    """
    View para download de PDF da GRU.
    
    📍 URL: /gru/download/<arquivo>/
    """
    
    def get(self, request, arquivo):
        """Download do arquivo PDF"""
        try:
            # Validar nome do arquivo (segurança)
            if '..' in arquivo or '/' in arquivo:
                logger.warning(f"Tentativa de acesso inválido ao arquivo: {arquivo}")
                return HttpResponse('Acesso negado', status=403)
            
            # Caminho do arquivo
            arquivo_path = f'media/gru_pdfs/{arquivo}'
            
            if not os.path.exists(arquivo_path):
                logger.warning(f"Arquivo não encontrado: {arquivo_path}")
                return HttpResponse('Arquivo não encontrado', status=404)
            
            # Abrir e retornar arquivo
            response = FileResponse(open(arquivo_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{arquivo}"'
            response['Content-Type'] = 'application/pdf'
            
            logger.info(f"PDF baixado: {arquivo} - Usuário: {request.user}")
            
            return response
            
        except Exception as e:
            logger.exception(f"Erro ao baixar PDF: {str(e)}")
            return HttpResponse('Erro ao baixar arquivo', status=500)


class CriarGRUView(LoginRequiredMixin, View):
    """
    View mínima para criar/gerar uma GRU a partir do formulário simples
    inserido na dashboard. Gera um PDF usando `GRUPDFGenerator` e
    redireciona para download.
    """

    def post(self, request):
        # Pré-processar alguns campos que podem chegar em formatos locais
        data = request.POST.copy()
        # Normalizar vírgula decimal
        if 'valor' in data and data.get('valor'):
            data['valor'] = data.get('valor').replace(',', '.')

        # Converter competência no formato YYYY-MM para YYYY-MM-01 (DateField)
        comp = data.get('competencia')
        if comp and len(comp) == 7 and comp.count('-') == 1:
            data['competencia'] = f"{comp}-01"

        # Preferir validar com ModelForm e persistir
        form = GRUModelForm(data)
        if form.is_valid():
            try:
                instancia = form.save(commit=False)
                instancia.criado_por = request.user
                instancia.status = 'PENDENTE'

                # Gerar PDF
                dados = {
                    'numero_gru': instancia.codigo_recolhimento or f"MANUAL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'valor': instancia.valor or Decimal('0.00'),
                    'valor_recolhido': Decimal('0.00'),
                    'data_vencimento': instancia.vencimento,
                    'data_pagamento': None,
                    'orgao_responsavel': instancia.beneficiario_nome or instancia.beneficiario_cpf,
                    'descricao_receita': instancia.descricao or 'GRU gerada manualmente',
                    'status': instancia.status,
                    'historia': []
                }

                # Primeira tentativa: gerar via API SISGRU usando JWT (se configurado)
                api_used = False
                try:
                    issuer = getattr(settings, 'SISGRU_JWT_ISSUER', None)
                    private_key_pem = getattr(settings, 'SISGRU_JWT_PRIVATE_KEY', None)
                    private_key_path = getattr(settings, 'SISGRU_JWT_PRIVATE_KEY_PATH', None)
                    endpoint_path = getattr(settings, 'SISGRU_GENERATE_PATH', 'gerar')

                    if private_key_path and not private_key_pem:
                        with open(private_key_path, 'r', encoding='utf-8') as f:
                            private_key_pem = f.read()

                    if issuer and private_key_pem:
                        service = SISGRUService('', '')
                        # preparar dados mínimos para API (tags esperadas podem variar)
                        dados_api = {
                            'ugArrecadadora': getattr(settings, 'SISGRU_UG_ARRECADADORA', ''),
                            'valor': str(instancia.valor),
                            'vencimento': instancia.vencimento.isoformat() if instancia.vencimento else '',
                            'descricao': instancia.descricao or '',
                        }
                        resp = service.gerar_gru_via_api(dados_api, issuer, private_key_pem, endpoint_path=endpoint_path)
                        # Se API retornar dados, atualiza instância com código/valores
                        if resp and resp.get('data'):
                            first = resp['data'][0]
                            # Tenta mapear campos retornados
                            codigo = first.get('id') or first.get('recolhimento') or first.get('codigo')
                            if codigo:
                                instancia.codigo_recolhimento = codigo
                            api_used = True

                except Exception as e:
                    logger.warning(f"Tentativa de geração via API falhou: {str(e)}")

                # Gerar PDF localmente (sempre que possível)
                pdf_dir = 'media/gru_pdfs'
                os.makedirs(pdf_dir, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                arquivo_nome = f"gru_{timestamp}.pdf"
                arquivo_path = os.path.join(pdf_dir, arquivo_nome)

                generator = GRUPDFGenerator()
                generator.gerar_pdf(dados, arquivo_path)

                # Salva caminho do arquivo no modelo (relative path para media/)
                instancia.pdf_file.name = f'gru_pdfs/{arquivo_nome}'
                instancia.save()

                messages.success(request, 'GRU gerada e salva com sucesso')
                return redirect('gru:download_pdf', arquivo=arquivo_nome)

            except Exception as e:
                logger.exception(f"Erro ao gerar GRU manualmente: {str(e)}")
                messages.error(request, f'Erro ao gerar GRU: {str(e)}')
                return redirect('gru:home')

        else:
            # Logar erros para facilitar diagnóstico
            logger.warning(f"Formulário GRU inválido: {form.errors.as_json()}")
            # Reexibir a página de criação com erros preservados
            return render(request, 'gru/create.html', {
                'form': form,
                'titulo': 'Gerar GRU',
                'descricao': 'Corrija os erros abaixo e tente novamente'
            }, status=400)

    def get(self, request):
        """Exibe a página de criação de GRU com o formulário."""
        form = GRUModelForm()
        return render(request, 'gru/create.html', {
            'form': form,
            'titulo': 'Gerar GRU',
            'descricao': 'Preencha os dados para gerar uma nova GRU'
        })


class ValidarGRUAPIView(LoginRequiredMixin, View):
    """
    API AJAX para validar número de GRU em tempo real.
    
    📍 URL: /gru/api/validar/
    """
    
    def post(self, request):
        """Validar número de GRU"""
        numero = request.POST.get('numero', '').strip()
        
        from .gru_service import SISGRUService
        
        service = SISGRUService('dummy', 'dummy')  # Não precisa credenciais para validar
        
        eh_valido = service.validar_numero_gru(numero)
        
        return JsonResponse({
            'valido': eh_valido,
            'numero': numero,
            'comprimento': len(numero.replace('.', '').replace('-', ''))
        })


class DisponibilidadeAPIView(LoginRequiredMixin, View):
    """
    API AJAX para verificar disponibilidade da API SISGRU.
    
    📍 URL: /gru/api/disponibilidade/
    """
    
    def get(self, request):
        """Verificar se API está disponível"""
        usuario = request.GET.get('usuario', '')
        senha = request.GET.get('senha', '')
        
        if not usuario or not senha:
            return JsonResponse({
                'disponivel': False,
                'mensagem': 'Credenciais não fornecidas'
            })
        
        try:
            service = SISGRUService(usuario, senha, producao=False)
            disponivel = service.verificar_disponibilidade()
            
            return JsonResponse({
                'disponivel': disponivel,
                'mensagem': '✓ API disponível' if disponivel else '✗ API indisponível'
            })
            
        except Exception as e:
            logger.error(f"Erro ao verificar disponibilidade: {str(e)}")
            return JsonResponse({
                'disponivel': False,
                'mensagem': f'Erro: {str(e)}'
            }, status=400)


class HistoricoGRUView(LoginRequiredMixin, ListView):
    """
    View para listar histórico de GRUs consultadas.
    
    ✅ Funcionalidades:
    - Listagem paginada
    - Filtros
    - Busca
    - Ordenação
    
    📍 URL: /gru/historico/
    
    TODO: Implementar quando criar modelo ConsultaGRU
    """
    
    template_name = 'gru/historico.html'
    paginate_by = 20
    context_object_name = 'consultas'
    
    def get_queryset(self):
        """Obter consultas do usuário"""
        qs = GRU.objects.all().order_by('-criado_em')

        # Aplicar filtros do formulário, se fornecidos
        form = FiltroGRUForm(self.request.GET)
        if form.is_valid():
            numero = form.cleaned_data.get('numero_gru')
            status = form.cleaned_data.get('status')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')
            valor_min = form.cleaned_data.get('valor_minimo')
            valor_max = form.cleaned_data.get('valor_maximo')

            if numero:
                qs = qs.filter(codigo_recolhimento__icontains=numero)
            if status:
                qs = qs.filter(status=status)
            if data_inicio:
                qs = qs.filter(criado_em__date__gte=data_inicio)
            if data_fim:
                qs = qs.filter(criado_em__date__lte=data_fim)
            if valor_min is not None:
                qs = qs.filter(valor__gte=valor_min)
            if valor_max is not None:
                qs = qs.filter(valor__lte=valor_max)

        return qs
    
    def get_context_data(self, **kwargs):
        """Adicionar filtros ao contexto"""
        context = super().get_context_data(**kwargs)
        context['form_filtro'] = FiltroGRUForm(self.request.GET)
        return context


class EstatisticasGRUView(LoginRequiredMixin, View):
    """
    View para exibir estatísticas de GRUs.
    
    📍 URL: /gru/estatisticas/
    """
    
    template_name = 'gru/estatisticas.html'
    
    def get(self, request):
        """Exibir estatísticas"""
        # TODO: Implementar quando criar modelo
        
        estatisticas = {
            'total_consultadas': 0,
            'total_pago': 0,
            'total_pendente': 0,
            'valor_total': 0,
            'valor_recolhido': 0,
        }
        
        return render(request, self.template_name, {
            'estatisticas': estatisticas,
            'titulo': 'Estatísticas de GRUs'
        })


# ==================== VIEWS AUXILIARES ====================

def gru_home(request):
    """Homepage do módulo GRU"""
    if not request.user.is_authenticated:
        return redirect('login')

    # Estatísticas reais usando o modelo GRU
    try:
        stats = {
            'pendentes': GRU.objects.filter(status='PENDENTE').count(),
            'pagas': GRU.objects.filter(status='PAGA').count(),
            'vencidas': GRU.objects.filter(status='VENCIDA').count(),
            'total_grus': GRU.objects.count(),
        }
    except Exception:
        stats = {
            'pendentes': 0,
            'pagas': 0,
            'vencidas': 0,
            'total_grus': 0,
        }

    # GRUs recentes do usuário
    recent_grus = []
    try:
        recent_grus = GRU.objects.filter(criado_por=request.user).order_by('-criado_em')[:8]
    except Exception:
        recent_grus = []

    return render(request, 'gru/home.html', {
        'titulo': 'Gerenciador de GRU',
        'descricao': 'Sistema de consulta e geração de Guias de Recolhimento da União',
        'stats': stats,
        'recent_grus': recent_grus,
    })


def gru_api_info(request):
    """Informações sobre a API SISGRU"""
    info = {
        'nome': 'SISGRU - Guia de Recolhimento da União',
        'versao': 'V1.0',
        'entidade': 'Ministério da Fazenda - Secretaria do Tesouro Nacional',
        'endpoint_producao': 'https://webservice.sisgru.tesouro.gov.br/sisgru/services/v1',
        'endpoint_homolog': 'https://webservice-sisgru-hml.tesouro.gov.br/sisgru/services/v1',
        'autenticacao': 'HTTP Basic Auth (Conecta.Gov.BR)',
        'disponibilidade': 'Segunda a sexta, 08:00-22:00 (horário Brasília, exceto feriados)',
        'operacoes': [
            'Pesquisar (consultar GRUs)',
            'Retificar (corrigir dados)',
            'Restituir (solicitar devolução)'
        ]
    }
    
    return JsonResponse(info)


# ==================== TRATAMENTO DE ERROS ====================

def error_404(request, exception):
    """Erro 404 customizado"""
    return render(request, 'gru/erro.html', {
        'codigo': 404,
        'mensagem': 'Página não encontrada'
    }, status=404)


def error_500(request):
    """Erro 500 customizado"""
    return render(request, 'gru/erro.html', {
        'codigo': 500,
        'mensagem': 'Erro interno do servidor'
    }, status=500)
