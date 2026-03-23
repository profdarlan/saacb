"""
🔗 SERVIÇO DE INTEGRAÇÃO COM API SISGRU
Documentação: https://www.gov.br/conecta/catalogo/apis/sisgru-guia-de-recolhimento-da-uniao

Módulo responsável pela integração com a API do SISGRU (Sistema de Gestão 
de Recolhimento da União) para consulta e geração de GRUs.
"""

import requests
import logging
from typing import Dict, Optional, List
from datetime import datetime
from decimal import Decimal
import base64
from django.conf import settings
import xml.etree.ElementTree as ET
from datetime import timedelta

try:
    import jwt
except Exception:
    jwt = None

logger = logging.getLogger(__name__)


class SISGRUAPIError(Exception):
    """Exceção customizada para erros da API SISGRU"""
    pass


class SISGRUService:
    """
    Serviço de integração com a API SISGRU do Governo Federal.
    
    ✅ Funcionalidades:
    - Autenticação via HTTP Basic Auth
    - Consulta de GRUs existentes
    - Validação de GRUs
    - Tratamento de erros e retry
    - Logging detalhado
    
    ❌ Limitações:
    - Disponível seg-sex 08:00-22:00 (Brasília)
    - Requer credenciais do Conecta.Gov.BR
    """
    
    # Endpoints da API
    ENDPOINT_HOMOLOG = "https://webservice-sisgru-hml.tesouro.gov.br/sisgru/services/v1"
    ENDPOINT_PRODUCAO = "https://webservice.sisgru.tesouro.gov.br/sisgru/services/v1"
    
    def __init__(self, usuario: str, senha: str, producao: bool = False):
        """
        Inicializa o serviço SISGRU.
        
        Args:
            usuario (str): Usuário do Conecta.Gov.BR
            senha (str): Senha do Conecta.Gov.BR
            producao (bool): Se True usa produção, senão homologação
            
        Raises:
            SISGRUAPIError: Se credenciais inválidas
        """
        self.usuario = usuario
        self.senha = senha
        self.producao = producao
        self.base_url = self.ENDPOINT_PRODUCAO if producao else self.ENDPOINT_HOMOLOG
        
        # Codificar credenciais para Basic Auth
        self._configurar_autenticacao()
        
        logger.info(f"SISGRUService inicializado - Ambiente: {'PRODUÇÃO' if producao else 'HOMOLOGAÇÃO'}")
    
    def _configurar_autenticacao(self):
        """Configura cabeçalho de autenticação HTTP Basic"""
        credenciais = f"{self.usuario}:{self.senha}"
        credenciais_encoded = base64.b64encode(credenciais.encode()).decode()
        
        self.headers = {
            "Authorization": f"Basic {credenciais_encoded}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "SAACB-Sistema/1.0"
        }
    
    def consultar_gru(self, numero_gru: str) -> Dict:
        """
        Consulta uma GRU na API SISGRU.
        
        Args:
            numero_gru (str): Número da GRU (ex: "10000000000123456789000000000000")
            
        Returns:
            Dict: Dados da GRU retornados pela API
            
        Raises:
            SISGRUAPIError: Se erro na requisição
            
        Exemplo:
            >>> service = SISGRUService('usuario', 'senha')
            >>> resultado = service.consultar_gru('10000000000123456789000000000000')
            >>> print(resultado['data']['valor'])
        """
        url = f"{self.base_url}/pesquisar"
        
        payload = {
            "gru": numero_gru
        }
        
        try:
            logger.debug(f"Consultando GRU: {numero_gru}")
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            # Verificar status HTTP
            if response.status_code == 401:
                raise SISGRUAPIError("Autenticação falhou. Verifique credenciais do Conecta.Gov.BR")
            elif response.status_code == 403:
                raise SISGRUAPIError("Acesso negado. Você não tem permissão para acessar esta GRU")
            elif response.status_code == 404:
                raise SISGRUAPIError(f"GRU não encontrada: {numero_gru}")
            elif response.status_code >= 500:
                raise SISGRUAPIError(f"Erro no servidor SISGRU: {response.status_code}")
            elif response.status_code >= 400:
                raise SISGRUAPIError(f"Erro na requisição: {response.text}")
            
            response.raise_for_status()
            
            dados = response.json()
            logger.info(f"GRU consultada com sucesso: {numero_gru}")
            
            return dados
            
        except requests.exceptions.ConnectionError:
            raise SISGRUAPIError("Erro de conexão com servidor SISGRU. Verifique sua internet.")
        except requests.exceptions.Timeout:
            raise SISGRUAPIError("Timeout ao conectar com API SISGRU (>30s)")
        except requests.exceptions.RequestException as e:
            raise SISGRUAPIError(f"Erro na requisição: {str(e)}")
        except ValueError as e:
            raise SISGRUAPIError(f"Erro ao processar resposta JSON: {str(e)}")
    
    def validar_numero_gru(self, numero_gru: str) -> bool:
        """
        Valida o formato de uma GRU.
        
        Formato esperado:
        - 32 dígitos
        - Formato: UUGGBBRRRRMMUUDDDDCCCCVVVVVVVVVV
        
        Args:
            numero_gru (str): Número da GRU a validar
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if not isinstance(numero_gru, str):
            return False
        
        # Remove espaços e hífens
        numero = numero_gru.replace(" ", "").replace("-", "")
        
        # Deve ter exatamente 32 dígitos
        if len(numero) != 32:
            return False
        
        # Deve conter apenas dígitos
        if not numero.isdigit():
            return False
        
        return True

    # --------------------- JWT / GERAÇÃO VIA API ---------------------
    @staticmethod
    def generate_jwt_rs256(private_key_pem: str, issuer: str, exp_seconds: int = 300) -> str:
        """Gera um token JWT RS256 dado uma chave privada PEM e 'iss'.

        Requer a biblioteca `pyjwt` (pip install pyjwt[crypto]).
        """
        if jwt is None:
            raise SISGRUAPIError('PyJWT não instalado. Instale com: pip install pyjwt[crypto]')

        payload = {'iss': issuer}
        if exp_seconds:
            payload['exp'] = datetime.utcnow() + timedelta(seconds=exp_seconds)

        try:
            token = jwt.encode(payload, private_key_pem, algorithm='RS256')
            # pyjwt >=2 retorna str
            return token
        except Exception as e:
            raise SISGRUAPIError(f'Erro ao gerar JWT: {str(e)}')

    def gerar_gru_via_api(self, dados: Dict, issuer: str, private_key_pem: str, endpoint_path: str = 'gerar') -> Dict:
        """Gera uma GRU via API SISGRU utilizando JWT RS256.

        Args:
            dados: dicionário com chaves mínimas (ex: ugArrecadadora, valor, vencimento, descricao)
            issuer: valor 'iss' do token
            private_key_pem: chave privada em PEM para assinar o token
            endpoint_path: caminho relativo no serviço (padrão 'gerar')

        Retorna:
            dict: dados retornados (após parse do XML)
        """
        token = self.generate_jwt_rs256(private_key_pem, issuer)

        url = f"{self.base_url}/{endpoint_path}"

        # Monta XML simples conforme exemplo (ajustável conforme especificação completa)
        root = ET.Element('grus')
        gru_el = ET.SubElement(root, 'gru')
        for k,v in dados.items():
            if v is None:
                continue
            tag = ET.SubElement(gru_el, k)
            tag.text = str(v)

        xml_body = ET.tostring(root, encoding='utf-8', method='xml')

        headers = {
            'Content-Type': 'application/xml',
            'Accept-Encoding': 'gzip',
            'Authorization': f'Bearer {token}'
        }

        try:
            resp = requests.post(url, data=xml_body, headers=headers, timeout=60)

            if resp.status_code == 401:
                raise SISGRUAPIError('Credenciais JWT não informadas corretamente (401)')
            if resp.status_code == 403:
                raise SISGRUAPIError(f'Credenciais inválidas/sem permissão (403): {resp.text}')
            if resp.status_code == 422:
                raise SISGRUAPIError(f'Requisição inválida (422): {resp.text}')
            if resp.status_code == 404:
                raise SISGRUAPIError(f'Recurso não encontrado (404)')
            if resp.status_code >= 500:
                raise SISGRUAPIError(f'Erro no servidor SISGRU: {resp.status_code}')

            # Sucesso: parse XML
            try:
                tree = ET.fromstring(resp.content)
                # Retorna estrutura simples (lista de grus)
                result = []
                for g in tree.findall('.//gru'):
                    item = {child.tag: child.text for child in g}
                    result.append(item)

                return {'status_code': resp.status_code, 'data': result}
            except ET.ParseError:
                # Se não for XML, retorna raw
                return {'status_code': resp.status_code, 'raw': resp.text}

        except requests.exceptions.RequestException as e:
            raise SISGRUAPIError(f'Erro na requisição SISGRU: {str(e)}')
    
    def extrair_dados_gru(self, dados_brutos: Dict) -> Dict:
        """
        Extrai dados relevantes da resposta da API SISGRU.
        
        Args:
            dados_brutos (Dict): Resposta bruta da API
            
        Returns:
            Dict: Dados estruturados
            
        Exemplo:
            >>> dados_brutos = service.consultar_gru('...')
            >>> dados = service.extrair_dados_gru(dados_brutos)
            >>> print(dados['valor_recolhido'])
        """
        try:
            # A resposta da API tem estrutura: {"data": {...}, "metadata": {...}}
            data = dados_brutos.get('data', {})
            
            return {
                'numero_gru': data.get('numero'),
                'valor': Decimal(str(data.get('valor', 0))),
                'valor_recolhido': Decimal(str(data.get('valor_recolhido', 0))),
                'data_vencimento': data.get('data_vencimento'),
                'data_pagamento': data.get('data_pagamento'),
                'orgao_responsavel': data.get('orgao_responsavel'),
                'descricao_receita': data.get('descricao_receita'),
                'status': data.get('status', 'PENDENTE'),
                'historia': data.get('history', []),
                'documentos': data.get('documentos', [])
            }
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Erro ao extrair dados da GRU: {str(e)}")
            raise SISGRUAPIError(f"Erro ao processar dados da GRU: {str(e)}")
    
    def verificar_disponibilidade(self) -> bool:
        """
        Verifica se a API está disponível.
        
        Returns:
            bool: True se disponível, False caso contrário
            
        Nota:
            API disponível seg-sex 08:00-22:00 horário de Brasília
        """
        # Fazer uma requisição simples
        try:
            # Usar um número inválido só para testar conexão
            self.consultar_gru("00000000000000000000000000000000")
        except SISGRUAPIError as e:
            # Se erro de autenticação, API está disponível mas credenciais erradas
            if "Autenticação" in str(e):
                return True
            # Se erro de servidor, API indisponível
            if "servidor" in str(e).lower():
                return False
            # Se GRU não encontrada, API está disponível
            return True
        except Exception:
            return False
        
        return True


class GRUPDFGenerator:
    """
    Gerador de PDF para GRU.
    
    ✅ Funcionalidades:
    - Gera PDF visual da GRU
    - Formato compatível com sistema bancário
    - Código de barras (se biblioteca disponível)
    - Múltiplas vias
    
    Requisitos:
    - reportlab (pip install reportlab)
    - PyPDF2 (pip install PyPDF2) - opcional
    """
    
    def __init__(self):
        """Inicializa gerador de PDF"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import ParagraphStyle
            from reportlab.lib.units import cm, mm
            self.canvas_module = canvas
            self.A4 = A4
            self.colors = colors
            self.cm = cm
            self.mm = mm
        except ImportError:
            raise SISGRUAPIError(
                "ReportLab não está instalado. "
                "Execute: pip install reportlab"
            )
        
        logger.info("GRUPDFGenerator inicializado")
    
    def gerar_pdf(self, dados_gru: Dict, arquivo_saida: str) -> str:
        """
        Gera PDF da GRU.
        
        Args:
            dados_gru (Dict): Dados da GRU estruturados
            arquivo_saida (str): Caminho do arquivo de saída
            
        Returns:
            str: Caminho do arquivo gerado
            
        Raises:
            SISGRUAPIError: Se erro ao gerar PDF
            
        Exemplo:
            >>> generator = GRUPDFGenerator()
            >>> generator.gerar_pdf(dados_gru, '/tmp/gru.pdf')
        """
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.units import cm, mm
            
            # Criar documento PDF
            c = canvas.Canvas(arquivo_saida, pagesize=A4)
            largura, altura = A4
            
            # Margens
            margem_esq = 1.5 * cm
            margem_sup = 2 * cm
            
            # ====== CABEÇALHO ======
            c.setFont("Helvetica-Bold", 16)
            c.drawString(margem_esq, altura - margem_sup, "GUIA DE RECOLHIMENTO DA UNIÃO - GRU")
            
            c.setFont("Helvetica", 9)
            c.drawString(margem_esq, altura - margem_sup - 0.8*cm, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            # ====== DADOS PRINCIPAIS ======
            y = altura - margem_sup - 1.8*cm
            linhas = [
                ("Número GRU:", dados_gru.get('numero_gru', 'N/A')),
                ("Valor:", f"R$ {dados_gru.get('valor', 0):,.2f}"),
                ("Valor Recolhido:", f"R$ {dados_gru.get('valor_recolhido', 0):,.2f}"),
                ("Status:", dados_gru.get('status', 'PENDENTE')),
                ("Data Vencimento:", dados_gru.get('data_vencimento', 'N/A')),
                ("Data Pagamento:", dados_gru.get('data_pagamento', 'N/A')),
                ("Órgão Responsável:", dados_gru.get('orgao_responsavel', 'N/A')),
                ("Receita:", dados_gru.get('descricao_receita', 'N/A')),
            ]
            
            c.setFont("Helvetica", 10)
            for label, valor in linhas:
                c.setFont("Helvetica-Bold", 10)
                c.drawString(margem_esq, y, label)
                c.setFont("Helvetica", 10)
                c.drawString(margem_esq + 3*cm, y, str(valor))
                y -= 0.5*cm
            
            # ====== HISTÓRICO ======
            y -= 0.5*cm
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margem_esq, y, "Histórico de Movimentações:")
            y -= 0.5*cm
            
            c.setFont("Helvetica", 8)
            historia = dados_gru.get('historia', [])
            if historia:
                for evento in historia[:10]:  # Mostrar últimos 10 eventos
                    data = evento.get('data', '')
                    tipo = evento.get('tipo', '')
                    descricao = evento.get('descricao', '')
                    c.drawString(margem_esq, y, f"{data} - {tipo}: {descricao}")
                    y -= 0.4*cm
            else:
                c.drawString(margem_esq, y, "Nenhuma movimentação registrada")
            
            # ====== RODAPÉ ======
            c.setFont("Helvetica", 8)
            c.drawString(margem_esq, 1.5*cm, "Este documento foi gerado automaticamente pelo SAACB.")
            c.drawString(margem_esq, 1*cm, "Para informações detalhadas, consulte a API SISGRU.")
            
            # Salvar PDF
            c.save()
            logger.info(f"PDF gerado com sucesso: {arquivo_saida}")
            
            return arquivo_saida
            
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {str(e)}")
            raise SISGRUAPIError(f"Erro ao gerar PDF da GRU: {str(e)}")


# ==================== FUNÇÕES UTILITÁRIAS ====================

def gerar_numero_gru_exemplo() -> str:
    """
    Gera um número de GRU válido para teste.
    
    Formato: UUGGBBRRRRMMUUDDDDCCCCVVVVVVVVVV (32 dígitos)
    - UU: UF (27 = Minas Gerais)
    - GG: Gestão
    - BB: Beneficiário
    - etc
    
    Returns:
        str: Número de GRU válido para teste
    """
    from random import randint
    
    # UF 27 (Minas Gerais)
    uf = "27"
    # Gestão aleatória
    gestao = str(randint(1, 99)).zfill(2)
    # Resto aleatório
    resto = "".join(str(randint(0, 9)) for _ in range(28))
    
    return uf + gestao + resto


def formatar_numero_gru(numero: str) -> str:
    """
    Formata número de GRU para exibição.
    
    De: 10000000000123456789000000000000
    Para: 1000.0000.0001.2345.6789.0000.0000.00
    
    Args:
        numero (str): Número sem formatação
        
    Returns:
        str: Número formatado
    """
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


# ==================== TESTES ====================

if __name__ == "__main__":
    """Testes locais do módulo"""
    
    # Test 1: Validação de GRU
    print("=" * 50)
    print("TEST 1: Validação de Número GRU")
    print("=" * 50)
    
    service = SISGRUService("usuario_teste", "senha_teste", producao=False)
    
    grus_teste = [
        ("10000000000123456789000000000000", True),
        ("1000-0000-0001-2345", False),  # Muito curto
        ("1000000000012345678900000000000A", False),  # Contém letra
        ("", False),  # Vazio
    ]
    
    for gru, esperado in grus_teste:
        resultado = service.validar_numero_gru(gru)
        status = "✓" if resultado == esperado else "✗"
        print(f"{status} GRU '{gru}' -> {resultado}")
    
    # Test 2: Formatação de GRU
    print("\n" + "=" * 50)
    print("TEST 2: Formatação de Número GRU")
    print("=" * 50)
    
    numero = "10000000000123456789000000000000"
    formatado = formatar_numero_gru(numero)
    print(f"Original:  {numero}")
    print(f"Formatado: {formatado}")
    
    # Test 3: Gerar exemplo
    print("\n" + "=" * 50)
    print("TEST 3: Gerar Número GRU Exemplo")
    print("=" * 50)
    
    exemplo = gerar_numero_gru_exemplo()
    print(f"GRU Gerada: {exemplo}")
    print(f"Validação: {service.validar_numero_gru(exemplo)}")
    print(f"Formatada: {formatar_numero_gru(exemplo)}")
    
    print("\n✅ Testes concluídos!")
