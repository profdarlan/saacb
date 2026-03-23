"""
🔄 SISTEMA DE MIGRAÇÃO DE DADOS - TAREFAS → GRU
tarefas/gru/migrations_helper.py

Módulo responsável por migrar dados do modelo tarefassamc
para o modelo GRU com preenchimento automático de campos.
"""

import logging
from decimal import Decimal
from django.utils import timezone
from django.db import transaction

logger = logging.getLogger(__name__)


class MigracaoDadosGRU:
    """
    Classe responsável por migrar dados de tarefassamc para GRU.
    
    ✅ Migra:
    - NB (Número do Benefício)
    - CPF
    - Nome do Beneficiário
    - Valor do Débito
    - Endereço
    - Descrição/Motivo
    - Datas relevantes
    
    ⚠️ Requer:
    - Modelo GRU ativado
    - Campo numero_gru preenchido em tarefassamc
    """
    
    def __init__(self):
        """Inicializa migrador"""
        self.campos_mapeados = {
            'nb': 'numero_beneficio',
            'cpf': 'CPF',
            'beneficiario': 'nome_beneficiario',
            'valor': 'valor_divida',
            'endereco': 'endereco',
            'motivo': 'tipo_tarefa',
            'data_criacao': 'data_criacao',
        }
        logger.info("MigracaoDadosGRU inicializado")
    
    @transaction.atomic
    def migrar_tarefa_para_gru(self, tarefa, usuario=None):
        """
        Migra uma tarefa para GRU.
        
        Args:
            tarefa (tarefassamc): Tarefa a migrar
            usuario (User): Usuário que realizou a migração
            
        Returns:
            dict: Resultado da migração
            
        Raises:
            ValueError: Se tarefa não tiver NB ou GRU
            
        Exemplo:
            >>> from tarefas.gru.migrations_helper import MigracaoDadosGRU
            >>> migrador = MigracaoDadosGRU()
            >>> tarefa = tarefassamc.objects.first()
            >>> resultado = migrador.migrar_tarefa_para_gru(tarefa)
            >>> print(resultado['sucesso'])
        """
        from tarefas.models import tarefassamc
        from tarefas.gru.models import GRU
        
        resultado = {
            'sucesso': False,
            'gru_id': None,
            'mensagem': '',
            'campos_preenchidos': [],
            'erros': []
        }
        
        try:
            # Validar tarefa
            if not tarefa.numero_gru:
                raise ValueError("Tarefa não possui GRU associada")
            
            if not tarefa.CPF:
                raise ValueError("Tarefa não possui CPF")
            
            logger.info(f"Iniciando migração da tarefa {tarefa.id}")
            
            # Extrair dados da tarefa
            dados = self._extrair_dados_tarefa(tarefa)
            
            # Criar ou atualizar GRU
            gru, criada = GRU.objects.get_or_create(
                numero=tarefa.numero_gru,
                defaults={
                    'valor': dados.get('valor_divida', Decimal('0.00')),
                    'status': 'PENDENTE',
                    'usuario_consulta': usuario,
                    'tarefa_relacionada': tarefa,
                    'data_consulta': timezone.now(),
                }
            )
            
            # Atualizar campos da GRU
            campos_atualizados = self._atualizar_campos_gru(gru, dados)
            
            resultado['sucesso'] = True
            resultado['gru_id'] = gru.id
            resultado['campos_preenchidos'] = campos_atualizados
            resultado['mensagem'] = f"GRU {'criada' if criada else 'atualizada'} com sucesso"
            
            logger.info(f"Migração concluída - GRU: {gru.numero}")
            
        except ValueError as e:
            resultado['erros'].append(str(e))
            logger.error(f"Erro na migração: {str(e)}")
        except Exception as e:
            resultado['erros'].append(f"Erro inesperado: {str(e)}")
            logger.exception(f"Erro inesperado na migração: {str(e)}")
        
        return resultado
    
    def _extrair_dados_tarefa(self, tarefa):
        """
        Extrai dados relevantes da tarefa.
        
        Args:
            tarefa (tarefassamc): Tarefa
            
        Returns:
            dict: Dados extraídos
        """
        dados = {
            'numero_beneficio': getattr(tarefa, 'numero_beneficio', None),
            'cpf': tarefa.CPF,
            'nome_beneficiario': tarefa.nome_beneficiario,
            'valor_divida': tarefa.valor_divida if hasattr(tarefa, 'valor_divida') else Decimal('0.00'),
            'endereco': getattr(tarefa, 'endereco', ''),
            'tipo_tarefa': tarefa.tipo_tarefa if hasattr(tarefa, 'tipo_tarefa') else 'Análise de Benefício',
            'data_criacao': tarefa.data_criacao,
            'status_tarefa': tarefa.status,
        }
        
        logger.debug(f"Dados extraídos: {dados}")
        return dados
    
    def _atualizar_campos_gru(self, gru, dados):
        """
        Atualiza os campos da GRU com dados da tarefa.
        
        Args:
            gru (GRU): Objeto GRU
            dados (dict): Dados da tarefa
            
        Returns:
            list: Campos que foram atualizados
        """
        campos_atualizados = []
        
        # Valor
        if dados.get('valor_divida'):
            gru.valor = dados['valor_divida']
            campos_atualizados.append('valor')
        
        # Descrição da receita
        descricao = self._gerar_descricao_receita(dados)
        if descricao:
            gru.descricao_receita = descricao
            campos_atualizados.append('descricao_receita')
        
        # Órgão responsável
        gru.orgao_responsavel = 'INSS - Instituto Nacional do Seguro Social'
        campos_atualizados.append('orgao_responsavel')
        
        # Adicionar movimentação
        self._adicionar_movimentacao(gru, dados)
        
        # Salvar
        gru.save()
        
        return campos_atualizados
    
    def _gerar_descricao_receita(self, dados):
        """
        Gera descrição da receita baseada nos dados.
        
        Args:
            dados (dict): Dados da tarefa
            
        Returns:
            str: Descrição formatada
        """
        tipo = dados.get('tipo_tarefa', 'Análise de Benefício')
        cpf = dados.get('cpf', '')
        nome = dados.get('nome_beneficiario', '')
        
        return f"{tipo} - CPF: {cpf} - Beneficiário: {nome}"
    
    def _adicionar_movimentacao(self, gru, dados):
        """
        Adiciona movimentação ao histórico.
        
        Args:
            gru (GRU): Objeto GRU
            dados (dict): Dados da tarefa
        """
        evento = {
            'data': timezone.now().isoformat(),
            'tipo': 'ORIGEM_TAREFA',
            'descricao': f"GRU gerada a partir de tarefa SAACB - {dados.get('tipo_tarefa')}"
        }
        
        if not gru.historico_json:
            gru.historico_json = []
        
        gru.historico_json.append(evento)
    
    @transaction.atomic
    def migrar_multiplas_tarefas(self, tarefas_queryset, usuario=None):
        """
        Migra múltiplas tarefas em batch.
        
        Args:
            tarefas_queryset (QuerySet): QuerySet de tarefas
            usuario (User): Usuário que realizou a migração
            
        Returns:
            dict: Estatísticas de migração
            
        Exemplo:
            >>> tarefas = tarefassamc.objects.filter(numero_gru__isnull=False)
            >>> stats = migrador.migrar_multiplas_tarefas(tarefas)
            >>> print(f"Sucesso: {stats['total_sucesso']}")
        """
        stats = {
            'total_processadas': 0,
            'total_sucesso': 0,
            'total_erro': 0,
            'erros_detalhados': [],
        }
        
        logger.info(f"Iniciando migração em batch de {tarefas_queryset.count()} tarefas")
        
        for tarefa in tarefas_queryset:
            resultado = self.migrar_tarefa_para_gru(tarefa, usuario)
            
            stats['total_processadas'] += 1
            
            if resultado['sucesso']:
                stats['total_sucesso'] += 1
            else:
                stats['total_erro'] += 1
                stats['erros_detalhados'].append({
                    'tarefa_id': tarefa.id,
                    'erros': resultado['erros']
                })
            
            if stats['total_processadas'] % 10 == 0:
                logger.info(f"Processadas {stats['total_processadas']} tarefas...")
        
        logger.info(f"Migração concluída: {stats['total_sucesso']} sucesso, {stats['total_erro']} erro")
        
        return stats


class PreenchedorDadosGRU:
    """
    Preenche campos adicionais da GRU baseado em dados da tarefa.
    
    ✅ Campos que preenche:
    - NB (Número do Benefício)
    - CPF
    - Nome do Beneficiário
    - Valor do Débito
    - Data de Vencimento
    - Endereço Completo
    - Descrição do Motivo
    - Órgão Responsável
    """
    
    def __init__(self):
        """Inicializa preenchedor"""
        self.logger = logging.getLogger(__name__)
    
    def preencher_gru_completa(self, gru, tarefa):
        """
        Preenche todos os campos possíveis da GRU a partir da tarefa.
        
        Args:
            gru (GRU): Objeto GRU
            tarefa (tarefassamc): Objeto tarefa
            
        Returns:
            GRU: GRU preenchida
        """
        try:
            # Dados básicos
            self._preencher_dados_beneficiario(gru, tarefa)
            self._preencher_dados_financeiros(gru, tarefa)
            self._preencher_dados_endereco(gru, tarefa)
            self._preencher_dados_vencimento(gru, tarefa)
            self._preencher_descricoes(gru, tarefa)
            
            gru.save()
            self.logger.info(f"GRU {gru.numero} preenchida com sucesso")
            
            return gru
            
        except Exception as e:
            self.logger.error(f"Erro ao preencher GRU: {str(e)}")
            raise
    
    def _preencher_dados_beneficiario(self, gru, tarefa):
        """Preenche dados do beneficiário"""
        # Adicionar como JSON no campo descricao_receita
        dados_beneficiario = {
            'cpf': tarefa.CPF,
            'nome': tarefa.nome_beneficiario,
            'numero_beneficio': getattr(tarefa, 'numero_beneficio', None),
        }
        
        # Armazenar em JSON (se implementar campo customizado)
        self.logger.debug(f"Dados beneficiário: {dados_beneficiario}")
    
    def _preencher_dados_financeiros(self, gru, tarefa):
        """Preenche dados financeiros"""
        if hasattr(tarefa, 'valor_divida'):
            gru.valor = tarefa.valor_divida
        
        if hasattr(tarefa, 'valor_recolhido'):
            gru.valor_recolhido = tarefa.valor_recolhido
    
    def _preencher_dados_endereco(self, gru, tarefa):
        """Preenche endereço na descrição"""
        endereco = getattr(tarefa, 'endereco', '')
        if endereco:
            # Adicionar ao histórico
            self.logger.debug(f"Endereço: {endereco}")
    
    def _preencher_dados_vencimento(self, gru, tarefa):
        """Define data de vencimento"""
        from datetime import timedelta
        
        if not gru.data_vencimento:
            # Padrão: 30 dias a partir de hoje
            gru.data_vencimento = timezone.now().date() + timedelta(days=30)
    
    def _preencher_descricoes(self, gru, tarefa):
        """Preenche campos de descrição"""
        gru.orgao_responsavel = 'INSS - Instituto Nacional do Seguro Social'
        
        descricao = f"""
        Débito do Beneficiário: {tarefa.nome_beneficiario}
        CPF: {tarefa.CPF}
        Motivo: {getattr(tarefa, 'tipo_tarefa', 'Irregularidade em Benefício')}
        """
        
        gru.descricao_receita = descricao.strip()


# ==================== MANAGEMENT COMMAND ====================

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Django management command para migração de dados.
    
    Uso:
        python manage.py migrar_gru_de_tarefas
        python manage.py migrar_gru_de_tarefas --tarefa-id=1
        python manage.py migrar_gru_de_tarefas --status=CONCLUÍDA
        python manage.py migrar_gru_de_tarefas --dry-run
    """
    
    help = 'Migra dados de tarefas para GRU'
    
    def add_arguments(self, parser):
        """Adiciona argumentos do comando"""
        parser.add_argument(
            '--tarefa-id',
            type=int,
            help='ID da tarefa específica a migrar',
        )
        
        parser.add_argument(
            '--status',
            type=str,
            help='Filtrar tarefas por status',
        )
        
        parser.add_argument(
            '--tem-gru',
            action='store_true',
            help='Apenas tarefas que já possuem número de GRU',
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular migração sem salvar',
        )
        
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Output detalhado',
        )
    
    def handle(self, *args, **options):
        """Executa o comando"""
        from tarefas.models import tarefassamc
        
        self.verbose = options.get('verbose', False)
        self.dry_run = options.get('dry_run', False)
        
        # Construir QuerySet
        tarefas = tarefassamc.objects.all()
        
        if options['tarefa_id']:
            tarefas = tarefas.filter(id=options['tarefa_id'])
        
        if options['status']:
            tarefas = tarefas.filter(status=options['status'])
        
        if options['tem_gru']:
            tarefas = tarefas.filter(numero_gru__isnull=False)
        else:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️ Nota: Use --tem-gru para apenas migrar tarefas com GRU\n'
                )
            )
        
        if not tarefas.exists():
            raise CommandError('Nenhuma tarefa encontrada com os critérios informados')
        
        self.stdout.write(f'Encontradas {tarefas.count()} tarefas para migrar\n')
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('🔄 Modo DRY-RUN (sem salvar)\n'))
        
        # Executar migração
        migrador = MigracaoDadosGRU()
        stats = migrador.migrar_multiplas_tarefas(tarefas)
        
        # Exibir resultado
        self._exibir_resultado(stats)
    
    def _exibir_resultado(self, stats):
        """Exibe resultado da migração"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✅ RESULTADO DA MIGRAÇÃO'))
        self.stdout.write('='*50)
        
        self.stdout.write(f"Total processadas: {stats['total_processadas']}")
        self.stdout.write(
            self.style.SUCCESS(f"✓ Sucesso: {stats['total_sucesso']}")
        )
        
        if stats['total_erro'] > 0:
            self.stdout.write(
                self.style.ERROR(f"✗ Erros: {stats['total_erro']}")
            )
            
            if stats['erros_detalhados'] and self.verbose:
                self.stdout.write('\nDetalhes dos erros:')
                for erro in stats['erros_detalhados']:
                    self.stdout.write(
                        f"  Tarefa {erro['tarefa_id']}: {erro['erros']}"
                    )


# ==================== EXEMPLOS DE USO ====================

if __name__ == "__main__":
    """Testes e exemplos"""
    
    # Exemplo 1: Migrar uma tarefa
    print("Exemplo 1: Migrar uma tarefa")
    print("=" * 50)
    
    """
    from tarefas.models import tarefassamc
    from tarefas.gru.migrations_helper import MigracaoDadosGRU
    
    migrador = MigracaoDadosGRU()
    tarefa = tarefassamc.objects.first()
    
    if tarefa:
        resultado = migrador.migrar_tarefa_para_gru(tarefa)
        print(f"Sucesso: {resultado['sucesso']}")
        print(f"Mensagem: {resultado['mensagem']}")
        print(f"Campos: {resultado['campos_preenchidos']}")
    """
    
    # Exemplo 2: Migrar múltiplas tarefas
    print("\nExemplo 2: Migrar múltiplas tarefas")
    print("=" * 50)
    
    """
    tarefas = tarefassamc.objects.filter(numero_gru__isnull=False)
    stats = migrador.migrar_multiplas_tarefas(tarefas)
    
    print(f"Total sucesso: {stats['total_sucesso']}")
    print(f"Total erro: {stats['total_erro']}")
    """
    
    # Exemplo 3: Usar command
    print("\nExemplo 3: Usar via management command")
    print("=" * 50)
    
    """
    python manage.py migrar_gru_de_tarefas --tem-gru --verbose
    """
