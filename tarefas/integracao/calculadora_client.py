"""
Cliente Python para API de Cálculos SAACB
Integração com planilha_saacb (FastAPI)
"""
import os
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class APIException(Exception):
    """Exceção personalizada para erros da API"""
    pass


@dataclass
class BeneficiarioData:
    """Dados do beneficiário para cálculo"""
    numero_beneficio: str
    nome_titular: str
    periodo_debito_inicio: str
    periodo_debito_fim: str
    is_recebimento_indevido: bool = False


@dataclass
class CreditoData:
    """Dados de um crédito para cálculo"""
    competencia: str
    periodo_inicio: Optional[str] = None
    periodo_fim: Optional[str] = None
    valor_original: float = 0.0
    tem_decimo: bool = False


@dataclass
class IndiceData:
    """Dados de um índice de correção"""
    competencia: str
    indice: float


@dataclass
class CalculoResultado:
    """Resultado do cálculo"""
    id: str
    timestamp: str
    beneficiario: BeneficiarioData
    resultados: List[Dict]
    total_original: float
    total_corrigido: float
    diferenca: float

    @property
    def tem_resultados(self) -> bool:
        return len(self.resultados) > 0

    @property
    def quantidade_creditos(self) -> int:
        return len(self.resultados)


class CalculadoraClient:
    """
    Cliente para comunicação com a API de Cálculos
    """

    def __init__(self, api_url: Optional[str] = None, api_token: Optional[str] = None):
        """
        Inicializa o cliente

        Args:
            api_url: URL da API (ex: http://192.168.1.51:8002)
            api_token: Token de autenticação (opcional)
        """
        self.api_url = api_url or os.getenv('CALCULADORA_API_URL', 'http://localhost:8002')
        self.api_token = api_token or os.getenv('CALCULADORA_API_TOKEN')
        self.timeout = 30  # segundos

        # URLs base
        self.base_url = self.api_url.rstrip('/')
        self.endpoints = {
            'calcular': f'{self.base_url}/api/calcular',
            'gerar_excel': f'{self.base_url}/api/gerar-excel',
            'gerar_pdf': f'{self.base_url}/api/gerar-relatorio-pdf',
            'indices_padrao': f'{self.base_url}/api/indices-padrao',
        }

    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers com token se configurado"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if self.api_token:
            headers['X-API-TOKEN'] = self.api_token
        return headers

    def _tratar_erro(self, response: requests.Response, operacao: str) -> None:
        """
        Trata erro da API e lança exceção apropriada

        Args:
            response: Response da requisição
            operacao: Nome da operação (ex: "calcular")

        Raises:
            APIException: Com detalhes do erro
        """
        try:
            error_data = response.json()
            detalhe = error_data.get('detail', 'Erro desconhecido')
        except:
            detalhe = response.text

        raise APIException(
            f"Erro ao {operacao}: HTTP {response.status_code} - {detalhe}"
        )

    def ping(self) -> bool:
        """
        Verifica se a API está respondendo

        Returns:
            bool: True se API está online
        """
        try:
            response = requests.get(f'{self.base_url}/', timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def calcular(
        self,
        beneficiario: BeneficiarioData,
        creditos: List[CreditoData],
        indices: List[IndiceData]
    ) -> CalculoResultado:
        """
        Realiza cálculo de correção de créditos

        Args:
            beneficiario: Dados do beneficiário
            creditos: Lista de créditos
            indices: Lista de índices de correção

        Returns:
            CalculoResultado: Resultado do cálculo

        Raises:
            APIException: Em caso de erro na API
        """
        payload = {
            'beneficiario': {
                'numero_beneficio': beneficiario.numero_beneficio,
                'nome_titular': beneficiario.nome_titular,
                'periodo_debito_inicio': beneficiario.periodo_debito_inicio,
                'periodo_debito_fim': beneficiario.periodo_debito_fim,
                'is_recebimento_indevido': beneficiario.is_recebimento_indevido,
            },
            'creditos': [
                {
                    'competencia': c.competencia,
                    'periodo_inicio': c.periodo_inicio,
                    'periodo_fim': c.periodo_fim,
                    'valor_original': c.valor_original,
                }
                for c in creditos
            ],
            'indices': [
                {
                    'competencia': i.competencia,
                    'indice': i.indice,
                }
                for i in indices
            ]
        }

        try:
            response = requests.post(
                self.endpoints['calcular'],
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout
            )

            if not response.ok:
                self._tratar_erro(response, 'calcular créditos')

            data = response.json()

            return CalculoResultado(
                id=data['id'],
                timestamp=data['timestamp'],
                beneficiario=BeneficiarioData(**data['beneficiario']),
                resultados=data['resultados'],
                total_original=data['total_original'],
                total_corrigido=data['total_corrigido'],
                diferenca=data['diferenca']
            )

        except requests.Timeout:
            raise APIException(f"Timeout ao calcular créditos (>{self.timeout}s)")
        except requests.RequestException as e:
            raise APIException(f"Erro de conexão: {str(e)}")

    def gerar_excel(self, calculo: CalculoResultado) -> bytes:
        """
        Gera arquivo Excel do cálculo

        Args:
            calculo: Resultado do cálculo

        Returns:
            bytes: Conteúdo do Excel

        Raises:
            APIException: Em caso de erro na API
        """
        payload = {
            'beneficiario': {
                'numero_beneficio': calculo.beneficiario.numero_beneficio,
                'nome_titular': calculo.beneficiario.nome_titular,
                'periodo_debito_inicio': calculo.beneficiario.periodo_debito_inicio,
                'periodo_debito_fim': calculo.beneficiario.periodo_debito_fim,
                'is_recebimento_indevido': calculo.beneficiario.is_recebimento_indevido,
            },
            'creditos': [
                {
                    'competencia': r['competencia'],
                    'periodo_inicio': r.get('periodo_inicio'),
                    'periodo_fim': r.get('periodo_fim'),
                    'valor_original': r['valor_original'],
                }
                for r in calculo.resultados
            ],
            'indices': [
                {
                    'competencia': r['competencia'],
                    'indice': r['indice_correcao'],
                }
                for r in calculo.resultados
            ]
        }

        try:
            response = requests.post(
                self.endpoints['gerar_excel'],
                json=payload,
                headers=self._get_headers(),
                timeout=60  # PDF/Excel pode demorar mais
            )

            if not response.ok:
                self._tratar_erro(response, 'gerar Excel')

            return response.content

        except requests.Timeout:
            raise APIException(f"Timeout ao gerar Excel (>{60}s)")
        except requests.RequestException as e:
            raise APIException(f"Erro de conexão: {str(e)}")

    def gerar_pdf(self, calculo: CalculoResultado) -> bytes:
        """
        Gera arquivo PDF do cálculo

        Args:
            calculo: Resultado do cálculo

        Returns:
            bytes: Conteúdo do PDF

        Raises:
            APIException: Em caso de erro na API
        """
        payload = {
            'beneficiario': {
                'numero_beneficio': calculo.beneficiario.numero_beneficio,
                'nome_titular': calculo.beneficiario.nome_titular,
                'periodo_debito_inicio': calculo.beneficiario.periodo_debito_inicio,
                'periodo_debito_fim': calculo.beneficiario.periodo_debito_fim,
                'is_recebimento_indevido': calculo.beneficiario.is_recebimento_indevido,
            },
            'creditos': [
                {
                    'competencia': r['competencia'],
                    'periodo_inicio': r.get('periodo_inicio'),
                    'periodo_fim': r.get('periodo_fim'),
                    'valor_original': r['valor_original'],
                }
                for r in calculo.resultados
            ],
            'indices': [
                {
                    'competencia': r['competencia'],
                    'indice': r['indice_correcao'],
                }
                for r in calculo.resultados
            ]
        }

        try:
            response = requests.post(
                self.endpoints['gerar_pdf'],
                json=payload,
                headers=self._get_headers(),
                timeout=60
            )

            if not response.ok:
                self._tratar_erro(response, 'gerar PDF')

            return response.content

        except requests.Timeout:
            raise APIException(f"Timeout ao gerar PDF (>{60}s)")
        except requests.RequestException as e:
            raise APIException(f"Erro de conexão: {str(e)}")

    def obter_indices_padrao(self) -> Dict[str, float]:
        """
        Obtém índices padrão configurados

        Returns:
            Dict[str, float]: Dicionário de índices {competencia: indice}

        Raises:
            APIException: Em caso de erro na API
        """
        try:
            response = requests.get(
                self.endpoints['indices_padrao'],
                headers=self._get_headers(),
                timeout=10
            )

            if not response.ok:
                self._tratar_erro(response, 'obter índices padrão')

            data = response.json()
            return data.get('indices', {})

        except requests.RequestException as e:
            raise APIException(f"Erro de conexão: {str(e)}")


# ============= FUNÇÕES DE CONVERSÃO =============

def tarefa_para_calculo(tarefa) -> tuple[BeneficiarioData, List[CreditoData]]:
    """
    Converte uma Tarefa Django para dados de cálculo

    Args:
        tarefa: Instância de TarefaSAMC

    Returns:
        tuple: (BeneficiarioData, List[CreditoData])
    """
    # Beneficiário
    beneficiario = BeneficiarioData(
        numero_beneficio=tarefa.nb1 or tarefa.nb2 or '',
        nome_titular=tarefa.nome_interessado or '',
        periodo_debito_inicio='',
        periodo_debito_fim='',
        is_recebimento_indevido=False
    )

    # Créditos
    creditos = []
    if tarefa.valor and tarefa.Competencia:
        try:
            valor = float(str(tarefa.valor).replace('.', '').replace(',', '.'))
            creditos.append(CreditoData(
                competencia=tarefa.Competencia.strftime('%m/%Y') if hasattr(tarefa.Competencia, 'strftime') else tarefa.Competencia,
                periodo_inicio=tarefa.Periodo_irregular,
                periodo_fim=tarefa.Periodo_irregular,
                valor_original=valor,
            ))
        except (ValueError, AttributeError):
            pass

    return beneficiario, creditos


def gerar_indices_padrao_dummy() -> List[IndiceData]:
    """
    Gera índices dummy para teste
    Em produção, usar os índices reais da API

    Returns:
        List[IndiceData]: Lista de índices de exemplo
    """
    return [
        IndiceData(competencia=f'{mes:02d}/2002', indice=1.045)
        for mes in range(1, 13)
    ]
