# 🧠 MAPEAMENTO DO SISTEMA SAACB - Guia para IA

**Versão:** 1.0  
**Data:** 2026-03-21  
**Objetivo:** Documento completo para IA entender e depurar o sistema SAACB

---

## 📋 ÍNDICE

1. [Visão Geral do Sistema](#1-visão-geral-do-sistema)
2. [Arquitetura e Estrutura](#2-arquitetura-e-estrutura)
3. [Tecnologias Utilizadas](#3-tecnologias-utilizadas)
4. [Modelos de Dados](#4-modelos-de-dados)
5. [URLs e Rotas](#5-urls-e-rotas)
6. [Integrações Externas](#6-integrações-externas)
7. [Fluxos de Trabalho](#7-fluxos-de-trabalho)
8. [Erros Conhecidos e Soluções](#8-erros-conhecidos-e-soluções)
9. [Pontos de Atenção para Debug](#9-pontos-de-atenção-para-debug)
10. [Comandos Úteis](#10-comandos-úteis)
11. [Recursos de Referência](#11-recursos-de-referência)

---

## 1. VISÃO GERAL DO SISTEMA

### 1.1 O que é SAACB?

**Sistema de Análises e Gestão de GRUs** para o INSS (Instituto Nacional do Seguro Social)

**Objetivo Principal:**
- Gerenciar tarefas de análise administrativa de benefícios
- Controlar GRUs (Guias de Recolhimento da União)
- Calcular créditos devidos e correções monetárias
- Gerar documentos oficiais (ofícios, despachos)
- Integrar com APIs governamentais (SISGRU)

### 1.2 Usuários do Sistema

- **Analistas do INSS:** Acessam tarefas, atualizam status, calculam créditos
- **Administradores:** Gerenciam usuários, configuram o sistema
- **Sistema:** Integrações automáticas com APIs externas

### 1.3 Funcionalidades Principais

| Funcionalidade | Descrição |
|----------------|-----------|
| Gestão de Tarefas | CRUD completo de tarefas de análise |
| Geração de Documentos | Ofícios, despachos, documentos variados |
| Consulta de GRUs | Integração com SISGRU (Governo Federal) |
| Cálculo de Créditos | Correção monetária automática via API |
| Import/Export | CSV de tarefas |
| Dashboard | Estatísticas e métricas |

---

## 2. ARQUITETURA E ESTRUTURA

### 2.1 Estrutura de Diretórios

```
projeto-saacb/
├── projeto_saacb/              # Configuração Django
│   ├── __init__.py
│   ├── settings.py             # Configurações principais
│   ├── settings_prod.py        # Configurações produção
│   ├── urls.py                # Rotas principais
│   └── wsgi.py                # WSGI para deploy
│
├── tarefas/                    # Aplicação principal
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Views principais
│   ├── views_integracao.py     # Views de integração (cálculos)
│   ├── admin.py               # Configuração Django Admin
│   ├── urls.py                # Rotas da app tarefas
│   ├── urls_integracao.py     # Rotas de integração
│   ├── forms.py               # Formulários
│   ├── services.py            # Lógica de negócio (documentos)
│   ├── utils.py               # Utilitários (PDF)
│   ├── signals.py             # Signals Django
│   ├── gru/                   # Módulo GRU (SISGRU)
│   │   ├── gru_service.py     # Serviço SISGRU
│   │   ├── views.py           # Views GRU
│   │   ├── urls.py            # Rotas GRU
│   │   └── forms.py           # Formulários GRU
│   ├── integracao/            # Integração calculadora
│   │   ├── calculadora_client.py  # Cliente API cálculos
│   │   └── __init__.py
│   ├── templates/             # Templates da app
│   │   └── tarefas/
│   │       ├── tarefa_list.html
│   │       ├── tarefa_detail.html
│   │       ├── tarefa_form.html
│   │       └── integracao/    # Templates de integração
│   │           └── calcular_creditos.html
│   ├── gru/                   # Templates GRU
│   │   └── gru_consulta.html
│   ├── templatetags/          # Template tags customizadas
│   └── migrations/            # Migrations do banco
│
├── templates/                 # Templates globais
│   ├── base.html              # Base HTML
│   └── design-system/         # Componentes UI
│       ├── button.html
│       ├── card.html
│       ├── badge.html
│       ├── stat-card.html
│       └── empty-state.html
│
├── static/                    # Arquivos estáticos
│   ├── css/
│   │   ├── style.css
│   │   ├── style2.css
│   │   └── design-system.css
│   └── admin/
│       ├── css/               # CSS customizado admin
│       └── js/                # JS customizado admin
│
├── media/                     # Arquivos de upload
│   └── gru_pdfs/              # PDFs de GRUs
│   └── relatorios_calculos/   # Relatórios de cálculo
│
├── data/                      # Dados persistentes (Docker)
│   └── db.sqlite3             # Banco de dados
│
├── docs/                      # Documentação
│   └── DESIGN-SYSTEM.md
│
├── manage.py                  # CLI Django
├── requirements.txt           # Dependências Python
├── Dockerfile                 # Configuração Docker
├── docker-compose.yml         # Orquestração Docker
└── .env                       # Variáveis de ambiente
```

### 2.2 Apps Django

| App | Descrição | Status |
|-----|-----------|--------|
| `django.contrib.admin` | Interface administrativa | ✅ Ativo |
| `django.contrib.auth` | Autenticação | ✅ Ativo |
| `django.contrib.contenttypes` | Tipos de conteúdo | ✅ Ativo |
| `django.contrib.sessions` | Sessões | ✅ Ativo |
| `django.contrib.messages` | Mensagens | ✅ Ativo |
| `django.contrib.staticfiles` | Arquivos estáticos | ✅ Ativo |
| `tarefas` | App principal | ✅ Ativo |

### 2.3 Middleware Stack

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Static files em produção
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Notas Importantes:**
- **WhiteNoise** está na 2ª posição (apenas após SecurityMiddleware)
- Essencial para servir static files em produção

---

## 3. TECNOLOGIAS UTILIZADAS

### 3.1 Backend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.11+ | Linguagem principal |
| Django | 4.2.7 | Framework web |
| Gunicorn | 22.0.0 | WSGI Server |
| WhiteNoise | 6.6.0 | Static files |
| SQLite | - | Banco de dados (desenvolvimento) |

### 3.2 Frontend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Bootstrap | 5 | Framework CSS |
| Design System | Custom | Componentes UI (identidade INSS) |
| jQuery | 3.6.0 | JavaScript (admin) |
| Select2 | - | Dropdowns customizados (admin) |

### 3.3 Integrações/APIs

| Serviço | Tecnologia | URL |
|---------|-----------|-----|
| SISGRU | SOAP/XML | `https://webservice.sisgru.tesouro.gov.br` |
| API Cálculos | FastAPI | `http://192.168.1.51:8002` |

### 3.4 Utilitários

| Biblioteca | Versão | Uso |
|-----------|--------|-----|
| requests | 2.31.0 | Requisições HTTP |
| python-dotenv | 1.0.1 | Variáveis de ambiente |
| num2words | 0.5.14 | Valores por extenso |
| xhtml2pdf | 0.2.17 | Geração de PDF (DESABILITADO) |
| pandas | 2.2.3 | Manipulação CSV/Excel |
| openpyxl | 3.1.5 | Excel moderno |
| xlrd | 2.0.1 | Excel legado |

---

## 4. MODELOS DE DADOS

### 4.1 Modelo Principal: `tarefassamc`

**Tabela:** `tarefas_tarefassamc`

**Campos Principais:**

| Campo | Tipo | Descrição | Obrigatório? |
|-------|------|-----------|--------------|
| `id` | BigAutoField | PK | ✅ |
| `nome_interessado` | CharField(100) | Nome do interessado | ❌ |
| `CPF` | CharField(20) | CPF | ❌ |
| `tarefa_n` | CharField(50) | Número da tarefa principal | ❌ |
| `tarefa_a` | CharField(50) | Tarefa anterior | ❌ |
| `sei_n` | CharField(50) | Número SEI | ❌ |
| `procj` | CharField(50) | Processo judicial | ❌ |
| `servico` | CharField(100) | Tipo de serviço (choices) | ❌ |
| `nome_tarefa` | FK(tipo_servico) | Fase da análise | ❌ |
| `nome_serv` | FK(nome_motiv) | Motivo do ressarcimento | ❌ |
| `der_tarefa` | CharField(20) | DER da tarefa | ❌ |
| `data_def` | CharField(20) | Data da ciência - ofício defesa | ❌ |
| `data_rec` | CharField(20) | Data da ciência - ofício recurso | ❌ |
| `nb1` | CharField(20) | Benefício 1 | ❌ |
| `nb2` | CharField(20) | Benefício 2 | ❌ |
| `sit_ben` | CharField(100) | Situação do benefício | ❌ |
| `aps` | CharField(100) | APS Manutenção | ❌ |
| `prazo` | CharField(100) | Prazo defesa (30/60 dias) | ❌ |
| `defesa_ap` | CharField(100) | Apresentou defesa? | ❌ |
| `categoria` | CharField(100) | Categoria da irregularidade | ❌ |
| `tip_con` | CharField(100) | Tipo de crédito (Dano ao Erário/Crédito) | ❌ |
| `oficio1` | DateField | Ofício Defesa - ciência | ❌ |
| `AR1` | TextField | Tipo do comprovante (AR Digital/Edital) | ❌ |
| `oficio2` | DateField | Ofício Recurso - ciência | ❌ |
| `AR2` | TextField | Tipo do comprovante | ❌ |
| `Competencia` | DateField | Competência | ❌ |
| `data_irregular` | DateField | Data início irregularidade | ❌ |
| `Periodo_irregular` | TextField | Período irregular | ❌ |
| `valor` | CharField(20) | Valor do débito | ❌ |
| `es_conc` | FK(conc_analise) | Conclusão da análise | ❌ |
| `obs1` | TextField | Relatório da defesa | ❌ |
| `obs2` | TextField | Direito e conclusão | ❌ |
| `resp_credito` | CharField(100) | Responsável pelo crédito | ❌ |
| `responsavel` | CharField(100) | Responsável legal | ❌ |
| `CPF_R` | CharField(20) | CPF responsável | ❌ |
| `Conclusao` | CharField(100) | Conclusão (REGULAR/IRREGULAR) | ❌ |
| `status` | CharField(100) | Status da tarefa | ❌ |
| `historico` | TextField | Fundamento da cobrança | ❌ |
| `env_serv` | CharField(50) | Envolvimento de servidor | ❌ |
| `servidor` | CharField(100) | Matrícula servidor | ❌ |
| `concluida_em` | DateField | Data de conclusão | ❌ |
| `atualizado_em` | DateTimeField | Última atualização | ✅ (auto_now) |
| `assigned_user` | FK(User) | Usuário responsável | ❌ |

#### Choices para `servico`:
```python
('ANALISE', "ANALISE"),
('ANALISE cobranca', "ANALISE - Cobrança"),
('ANALISE exigencia', "ANALISE - Exigência"),
('ANALISE corregedoria', "ANALISE - Corregedoria"),
('ANALISE pendencia', "ANALISE - Pendência"),
('ANALISE Concluir', "ANALISE - Concluir"),
('ANALISE recurso', "ANALISE - Recurso"),
('ANALISE judicial', "ANALISE - Judicial"),
('CONCLUIDO', "CONCLUIDO"),
('CONCLUIDO pendente', "CONCLUIDO - pendente"),
('PA', "PA - Aguardando Processo"),
('PARECER SOCIAL', "PARECER SOCIAL - Aguardando Parecer Social"),
('PERICIA', "PERICIA - Aguardando Perícia Médica"),
('PROCURADORIA', "PROCURADORIA - Aguardando Procuradoria"),
```

#### Choices para `status`:
```python
('PENDENTE', "PENDENTE"),
('PENDENTE', "PENDENTE - CORREÇÃO"),
('CONCLUIDA_INTERMEDIARIA', "CONCLUÍDA - INTERMEDIÁRIA"),
('CONCLUIDA_FINALIZADA', "CONCLUÍDA - FINALIZADA")
```

#### Choices para `Conclusao`:
```python
('REGULAR', "REGULAR"),
('IRREGULAR Boa fé', "IRREGULAR - Boa fé"),
('IRREGULAR Má fé', "IRREGULAR - Má fé"),
('PARCIALMENTE IRREGULAR', "PARCIALMENTE IRREGULAR"),
```

#### Choices para `tip_con`:
```python
('Crédito', "Crédito"),
('Dano ao Erário', "Dano ao Erário"),
```

### 4.2 Campos de Integração (Cálculos)

**Campos adicionados para integração com API de cálculos:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `valor_original_calculado` | DecimalField(12,2) | Valor original calculado |
| `valor_corrigido_calculado` | DecimalField(12,2) | Valor corrigido calculado |
| `valor_diferenca` | DecimalField(12,2) | Diferença calculada |
| `detalhes_calculo` | JSONField | Detalhes do cálculo (estruturado) |
| `relatorio_pdf` | FileField | Relatório PDF gerado |
| `calculado_em` | DateTimeField | Data/hora do cálculo |

**Estrutura do `detalhes_calculo` (JSONField):**
```json
{
  "id": "uuid-do-calculo",
  "timestamp": "2025-03-19T10:30:00",
  "resultados": [
    {
      "competencia": "01/2024",
      "valor_original": 1000.00,
      "valor_corrigido": 1050.00,
      "indice_correcao": 1.05
    }
  ]
}
```

### 4.3 Modelo: `GRU`

**Tabela:** `tarefas_gru`

| Campo | Tipo | Descrição | Obrigatório? |
|-------|------|-----------|--------------|
| `id` | BigAutoField | PK | ✅ |
| `beneficiario_nome` | CharField(200) | Nome do beneficiário | ❌ |
| `beneficiario_cpf` | CharField(30) | CPF do beneficiário | ❌ |
| `codigo_recolhimento` | CharField(64) | Código da GRU | ❌ |
| `competencia` | DateField | Competência | ❌ |
| `vencimento` | DateField | Data de vencimento | ❌ |
| `valor` | DecimalField(12,2) | Valor | ✅ (default=0) |
| `descricao` | TextField | Descrição | ❌ |
| `status` | CharField(20) | Status (PENDENTE/PAGA/VENCIDA/CANCELADA) | ✅ (default=PENDENTE) |
| `pdf_file` | FileField | PDF da GRU | ❌ |
| `criado_por` | FK(User) | Usuário que criou | ❌ |
| `criado_em` | DateTimeField | Data de criação | ✅ (auto_now_add) |
| `concluida_em` | DateTimeField | Data de conclusão | ❌ |
| `atualizado_em` | DateTimeField | Última atualização | ✅ (auto_now) |

### 4.4 Modelos de Apoio

#### `tipo_servico` - Tipos de serviços/fases de análise
```python
nome = CharField(100)
```

#### `nome_motiv` - Motivos de ressarcimento
```python
nome = CharField(100)
```

#### `conc_analise` - Conclusões de análise
```python
conc = CharField(100)           # Conclusão
conc_exp = TextField(blank=True) # Explicação detalhada
fim = CharField(100)            # PROCEDENTE/PARCIALMENTE PROCEDENTE/IMPROCEDENTE
```

#### `Role` - Funções de usuários
```python
name = CharField(100, unique=True)
description = TextField(blank=True)
```

#### `UserProfile` - Perfil do usuário
```python
user = OneToOneField(User)
role = ForeignKey(Role, blank=True, null=True)
```

---

## 5. URLS E ROTAS

### 5.1 Rotas Principais (`projeto_saacb/urls.py`)

| Path | View | Descrição |
|------|------|-----------|
| `/` | RedirectView | Redirect para `/tarefas/` |
| `/admin/` | admin.site.urls | Django Admin |
| `/tarefas/` | include(tarefas.urls) | App tarefas |
| `/gru/` | include(tarefas.gru.urls) | Módulo GRU |

### 5.2 Rotas da App `tarefas` (`tarefas/urls.py`)

**Namespace:** `tarefas`

| Path | View | Método | Descrição |
|------|------|--------|-----------|
| `/tarefas/` | TarefaListView | GET | Lista tarefas (clássico) |
| `/tarefas/lista/` | TarefaListOrdenadaView | GET | Lista tarefas (moderna, ordenável) |
| `/tarefas/<int:pk>/` | TarefaDetailView | GET | Detalhes da tarefa |
| `/tarefas/create/` | TarefaCreateView | GET/POST | Criar nova tarefa |
| `/tarefas/<int:pk>/update/` | TarefaUpdateView | GET/POST | Editar tarefa |
| `/tarefas/<int:pk>/delete/` | TarefaDeleteView | GET/POST | Deletar tarefa |
| `/tarefas/tarefa/<int:pk>/gerar/<str:tipo>/` | GerarDocumentoView | GET | Gerar documento (despacho/ofício) |
| `/tarefas/relatorios/por-usuario/` | RelatorioPorUsuarioView | GET | Relatório por usuário (PDF) |
| `/tarefas/relatorios/concluidas/` | RelatorioConcluidasView | GET | Relatório concluídas (PDF) |
| `/tarefas/export_csv/` | ExportCSVView | GET | Exportar CSV |
| `/tarefas/import_csv/` | ImportCSVView | POST | Importar CSV |

### 5.3 Rotas de Integração (`tarefas/urls.py`)

**Namespace:** `tarefas`

| Path | View | Método | Descrição |
|------|------|--------|-----------|
| `/tarefas/tarefa/<int:tarefa_id>/calcular/` | calcular_creditos_tarefa | GET/POST | Calcular créditos |
| `/tarefas/api/calcular/` | calcular_ajax | POST | Calcular via AJAX |
| `/tarefas/tarefa/<int:tarefa_id>/pdf/` | baixar_relatorio_pdf | POST | Baixar PDF de cálculo |
| `/tarefas/tarefa/<int:tarefa_id>/excel/` | baixar_relatorio_excel | POST | Baixar Excel de cálculo |
| `/tarefas/api/status/` | status_api | GET | Status da API de cálculos |

### 5.4 Rotas GRU (`tarefas/gru/urls.py`)

**Namespace:** `gru` (não configurado no projeto principal)

| Path | View | Método | Descrição |
|------|------|--------|-----------|
| `/gru/` | GRUListView | GET | Lista GRUs |
| `/gru/consultar/` | consultar_gru | POST | Consultar GRU |
| `/gru/<int:pk>/` | GRUDetailView | GET | Detalhes GRU |

### 5.5 URL Names

**Namespace: tarefas**

- `tarefas:tarefa_list`
- `tarefas:tarefa_list_moderna`
- `tarefas:tarefa_detail`
- `tarefas:tarefa_create`
- `tarefas:tarefa_update`
- `tarefas:tarefa_delete`
- `tarefas:gerar_documento`
- `tarefas:relatorio_usuario`
- `tarefas:relatorio_concluidas`
- `tarefas:export_csv`
- `tarefas:import_csv`
- `tarefas:integracao_calcular_creditos`
- `tarefas:integracao_api_calcular`
- `tarefas:integracao_baixar_pdf`
- `tarefas:integracao_baixar_excel`
- `tarefas:integracao_status_api`

---

## 6. INTEGRAÇÕES EXTERNAS

### 6.1 Integração SISGRU (API Governo)

**Arquivo:** `tarefas/gru/gru_service.py`

**Classe:** `SISGRUService`

**Endpoints:**
- **Homologação:** `https://webservice-sisgru-hml.tesouro.gov.br/sisgru/services/v1`
- **Produção:** `https://webservice-sisgru.tesouro.gov.br/sisgru/services/v1`

**Horário de funcionamento:** Seg-Sex, 08:00-22:00 (Horário de Brasília)

**Autenticação:** HTTP Basic Auth (Conecta.Gov.BR)

**Credenciais (settings.py):**
```python
SISGRU_USUARIO = os.environ.get('SISGRU_USUARIO')
SISGRU_SENHA = os.environ.get('SISGRU_SENHA')
SISGRU_PRODUCAO = os.environ.get('SISGRU_PRODUCAO', 'False') == 'True'
```

**Métodos principais:**

| Método | Descrição |
|--------|-----------|
| `consultar_gru(numero_gru)` | Consulta uma GRU |
| `validar_numero_gru(numero_gru)` | Valida formato de GRU |
| `gerar_gru_via_api(dados, issuer, private_key_pem)` | Gera GRU via JWT RS256 |
| `generate_jwt_rs256(private_key_pem, issuer)` | Gera token JWT |

**Formato de GRU (validação):**
- 32 dígitos
- Formato: `UUGGBBRRRRMMUUDDDDCCCCVVVVVVVVVV`

**Erros comuns:**

| Erro | Causa | Solução |
|------|-------|----------|
| HTTP 401 | Credenciais inválidas | Verificar usuário/senha |
| HTTP 403 | Sem permissão | Usuário não tem acesso |
| HTTP 404 | GRU não encontrada | Verificar número |
| HTTP 500 | Erro servidor SISGRU | Tentar novamente |
| Timeout | >30s | Verificar conexão |
| Fora do horário | Seg-Sex 08:00-22:00 | Aguardar horário |

### 6.2 Integração API de Cálculos (Planilha SAACB)

**Arquivo:** `tarefas/integracao/calculadora_client.py`

**Classe:** `CalculadoraClient`

**URL Base:** `http://192.168.1.51:8002` (configurável via `.env`)

**Credenciais (settings.py):**
```python
CALCULADORA_API_URL = os.getenv('CALCULADORA_API_URL', 'http://localhost:8002')
CALCULADORA_API_TOKEN = os.getenv('CALCULADORA_API_TOKEN')
```

**Endpoints:**

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/calcular` | POST | Calcular correção monetária |
| `/api/gerar-excel` | POST | Gerar Excel editável |
| `/api/gerar-relatorio-pdf` | POST | Gerar PDF de relatório |
| `/api/indices-padrao` | GET | Obter índices configurados |
| `/` | GET | Health check (ping) |

**Data Classes:**

```python
@dataclass
class BeneficiarioData:
    numero_beneficio: str
    nome_titular: str
    periodo_debito_inicio: str
    periodo_debito_fim: str
    is_recebimento_indevido: bool = False

@dataclass
class CreditoData:
    competencia: str
    periodo_inicio: Optional[str] = None
    periodo_fim: Optional[str] = None
    valor_original: float = 0.0
    tem_decimo: bool = False

@dataclass
class IndiceData:
    competencia: str
    indice: float

@dataclass
class CalculoResultado:
    id: str
    timestamp: str
    beneficiario: BeneficiarioData
    resultados: List[Dict]
    total_original: float
    total_corrigido: float
    diferenca: float
```

**Métodos principais:**

| Método | Descrição | Timeout |
|--------|-----------|---------|
| `ping()` | Verifica se API está online | 5s |
| `calcular(beneficiario, creditos, indices)` | Realiza cálculo | 30s |
| `gerar_excel(calculo)` | Gera Excel | 60s |
| `gerar_pdf(calculo)` | Gera PDF | 60s |
| `obter_indices_padrao()` | Obtém índices | 10s |

**Função de conversão:**

```python
def tarefa_para_calculo(tarefa) -> tuple[BeneficiarioData, List[CreditoData]]:
    """
    Converte uma Tarefa Django para dados de cálculo
    """
```

**Payload esperado pela API (exemplo):**

```json
{
  "beneficiario": {
    "numero_beneficio": "1234567890",
    "nome_titular": "João Silva",
    "periodo_debito_inicio": "",
    "periodo_debito_fim": "",
    "is_recebimento_indevido": false
  },
  "creditos": [
    {
      "competencia": "01/2024",
      "periodo_inicio": "01/2024",
      "periodo_fim": "12/2024",
      "valor_original": 1000.00
    }
  ],
  "indices": [
    {
      "competencia": "01/2024",
      "indice": 1.05
    }
  ]
}
```

**Resposta esperada (exemplo):**

```json
{
  "id": "uuid-calculo",
  "timestamp": "2025-03-19T10:30:00",
  "beneficiario": { ... },
  "resultados": [
    {
      "competencia": "01/2024",
      "valor_original": 1000.00,
      "valor_corrigido": 1050.00,
      "indice_correcao": 1.05
    }
  ],
  "total_original": 1000.00,
  "total_corrigido": 1050.00,
  "diferenca": 50.00
}
```

**Erros comuns:**

| Erro | Causa | Solução |
|------|-------|----------|
| APIException | Erro da API | Verificar payload |
| Timeout | >timeout | Aumentar timeout |
| ConnectionError | API offline | Verificar se API está rodando |
| ValueError | JSON inválido | Verificar resposta |

---

## 7. FLUXOS DE TRABALHO

### 7.1 Fluxo: Criar Tarefa

```
1. Usuário acessa /tarefas/create/
2. TarefaCreateView.render()
3. Formulário TarefaForm exibido
4. Usuário preenche campos
5. POST para /tarefas/create/
6. TarefaCreateView.form_valid()
   - assigned_user = request.user
   - Se status em STATUS_CONCLUIDOS:
     - concluida_em = timezone.now()
7. Salvar no banco
8. Redirect para /tarefas/
```

### 7.2 Fluxo: Atualizar Tarefa

```
1. Usuário acessa /tarefas/<id>/update/
2. TarefaUpdateView.render()
3. Formulário preenchido com dados existentes
4. Usuário modifica campos
5. POST para /tarefas/<id>/update/
6. TarefaUpdateView.form_valid()
   - instance = form.save(commit=False)
   - assigned_user = request.user
   - Se status em STATUS_CONCLUIDOS e sem concluida_em:
     - concluida_em = timezone.now()
   - instance.save()
7. Redirect para /tarefas/
```

### 7.3 Fluxo: Calcular Créditos (POST)

```
1. Usuário acessa /tarefas/tarefa/<id>/calcular/
2. calcular_creditos_tarefa.render()
   - Verifica se API está online (ping)
   - Exibe formulário de cálculo
3. Usuário clica "Calcular Créditos"
4. POST para /tarefas/tarefa/<id>/calcular/
5. calcular_creditos_tarefa.process()
   - Converter tarefa para dados de cálculo (tarefa_para_calculo)
   - Obter índices padrão (obter_indices_padrao)
   - Chamar API calcular()
   - Atualizar campos de integração:
     * valor_original_calculado
     * valor_corrigido_calculado
     * valor_diferenca
     * detalhes_calculo (JSON)
     * calculado_em
   - tarefa.save()
   - messages.success()
6. Se "gerar_pdf" checkbox:
   - Redirect para /tarefas/tarefa/<id>/pdf/
7. Senão:
   - Redirect para /tarefas/tarefa/<id>/
```

### 7.4 Fluxo: Calcular Créditos (AJAX)

```
1. JavaScript chama fetch('/tarefas/api/calcular/', { method: 'POST' })
2. calcular_ajax.process()
   - Extrai tarefa_id do POST
   - Converter tarefa para dados
   - Obter índices
   - Chamar API calcular()
   - Atualizar tarefa
   - Return JsonResponse com resultado
3. JavaScript atualiza UI com resultado
```

### 7.5 Fluxo: Baixar PDF de Cálculo

```
1. Usuário clica "Baixar PDF" ou botão no formulário
2. POST para /tarefas/tarefa/<id>/pdf/
3. baixar_relatorio_pdf.process()
   - Verifica se tarefa.detalhes_calculo existe
   - Reconstrói CalculoResultado do JSON
   - Chama client.gerar_pdf(resultado)
   - Recebe bytes do PDF
   - Return HttpResponse com content_type='application/pdf'
4. Browser faz download do arquivo
```

### 7.6 Fluxo: Consultar GRU

```
1. Usuário acessa /gru/
2. GRUListView.render()
3. Formulário de consulta
4. Usuário insere número da GRU
5. POST para /gru/consultar/
6. consultar_gru.process()
   - Instancia SISGRUService(usuario, senha, producao)
   - Valida formato da GRU (validar_numero_gru)
   - Chama service.consultar_gru(numero_gru)
   - Extrai dados estruturados (extrair_dados_gru)
   - Salva/Atualiza GRU no banco
   - Return template com resultados
```

### 7.7 Fluxo: Gerar Documento

```
1. Usuário acessa /tarefas/tarefa/<id>/gerar/<tipo>/
2. GerarDocumentoView.process()
   - tipo pode ser: despacho, oficio_recurso, etc.
   - Chama gerar_texto_documento(tarefa, tipo_doc)
3. gerar_texto_documento.process()
   - Carrega template do TEMPLATES dict (services.py)
   - Normaliza valor (parse float)
   - Converte para extenso (num2words)
   - Monta contexto com dados da tarefa
   - Aplica template.format(**contexto)
4. Se AJAX:
   - Return JsonResponse com texto
5. Senão:
   - Renderiza template exibir_documento.html
```

---

## 8. ERROS CONHECIDOS E SOLUÇÕES

### 8.1 Erro: `TemplateDoesNotExist: tarefas/calcular_creditos.html`

**Causa:** Template path incorreto em `views_integracao.py`

**Linha problemática (antiga):**
```python
# views_integracao.py, linha 107 e 120
return render(request, 'tarefas/calcular_creditos.html', { ... })
```

**Solução aplicada:**
```python
# Corrigido para
return render(request, 'tarefas/integracao/calcular_creditos.html', { ... })
```

**Arquivo:** `tarefas/views_integracao.py`

---

### 8.2 Erro: `NoReverseMatch: Reverse for 'tarefa_list' not found`

**Causa:** URL sem namespace em template

**Template problemático:** `tarefas/templates/tarefas/exibir_documento.html`

**Linha problemática (antiga):**
```django
{% url 'tarefa_list' %}
```

**Solução aplicada:**
```django
{% url 'tarefas:tarefa_list' %}
```

**Linhas corrigidas:** 14, 23, 63

---

### 8.3 Erro: `no such column: tarefas_tarefassamc.valor_original_calculado`

**Causa:** Migration de integração não aplicada

**Solução:**

```bash
# Opção 1: Aplicar migrations manualmente
docker exec -it saacb-app python manage.py migrate

# Opção 2: Executar script de correção
docker exec -it saacb-app python fix-migrations.py

# Opção 3: Recriar container
docker-compose down
docker-compose up -d --build
```

**Migration responsável:** `tarefas/migrations/0003_integracao_calculadora.py` (ou `0015_integracao_calculadora.py`)

**Campos adicionados pela migration:**
- `valor_original_calculado`
- `valor_corrigido_calculado`
- `valor_diferenca`
- `detalhes_calculo`
- `relatorio_pdf`
- `calculado_em`

---

### 8.4 Erro: API de Cálculos Indisponível

**Causa:** API de cálculos não está rodando ou URL incorreta

**Solução:**

1. Verificar se API está rodando:
```bash
curl http://192.168.1.51:8002/
```

2. Verificar configuração no `.env`:
```bash
CALCULADORA_API_URL=http://192.168.1.51:8002
```

3. Verificar se o container está rodando (Docker):
```bash
docker ps | grep planilha-calculos
```

4. Se não estiver rodando:
```bash
cd /path/to/planilha_saacb
uvicorn main:app --host 0.0.0.0 --port 8002
```

---

### 8.5 Erro: Static Files Não Encontradas (Produção)

**Causa:** `collectstatic` não executado ou WhiteNoise mal configurado

**Solução:**

```bash
# 1. Executar collectstatic
python manage.py collectstatic --noinput

# 2. Verificar settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← 2º lugar!
    # ... outros middlewares
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

### 8.6 Erro: SISGRU API Indisponível

**Causa:**
- Fora do horário de funcionamento (Seg-Sex 08:00-22:00 Brasília)
- Credenciais inválidas
- Erro de conexão

**Solução:**

1. Verificar horário:
```python
from datetime import datetime
import pytz

tz = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(tz)
print(f"Hora atual (Brasília): {agora.hour:02d}:{agora.minute:02d}")
```

2. Verificar credenciais no `.env`:
```bash
SISGRU_USUARIO=seu_usuario_conecta
SISGRU_SENHA=sua_senha_conecta
```

3. Verificar se está em produção ou homologação:
```bash
SISGRU_PRODUCAO=False  # True para produção
```

---

### 8.7 Erro: Database Locked (SQLite)

**Causa:** SQLite não suporta alta concorrência

**Solução temporária:**
```bash
# Copiar backup e sobrescrever
cp db.sqlite3 db.sqlite3.backup
```

**Solução definitiva:** Migrar para PostgreSQL

---

### 8.8 Erro: `AttributeError: 'NoneType' object has no attribute 'username'`

**Causa:** Campo `assigned_user` é None e código tenta acessar `assigned_user.username`

**Solução:** Acesso defensivo no código

```python
# ❌ Ruim
au = tarefa.assigned_user
username = au.username

# ✅ Bom
au = getattr(tarefa, 'assigned_user', None)
username = au.username if au else ''
```

**Arquivos afetados:** `views.py` (ExportCSVView), templates

---

### 8.9 Erro: Data Parsing Falha no CSV Import

**Causa:** Formato de data diferente do esperado

**Solução:** A função `try_parse_date` em `views.py` já tenta múltiplos formatos

**Formatos aceitos:**
- `YYYY-MM-DD` (ISO)
- `YYYY/MM/DD`
- `DD/MM/YYYY`
- `DD-MM-YYYY`
- `MM/DD/YYYY`
- `YYYYMMDD` (somente números)

---

### 8.10 Erro: PDF Desabilitado

**Causa:** `xhtml2pdf` desabilitado em `utils.py` devido a conflito de dependências

**Código atual:**
```python
# xhtml2pdf desabilitado temporariamente devido a conflito de dependências
# from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    return None  # PDF temporariamente desabilitado
```

**Solução:** Usar API de cálculos para gerar PDF ou corrigir dependências

---

## 9. PONTOS DE ATENÇÃO PARA DEBUG

### 9.1 Verificar Estado da Aplicação

```bash
# Django check
python manage.py check

# Django check deploy
python manage.py check --deploy

# Verificar migrations
python manage.py showmigrations

# Verificar aplicação de migrations
python manage.py showmigrations tarefas
```

### 9.2 Verificar Conexão com Banco

```python
# Django shell
python manage.py shell

from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM tarefas_tarefassamc")
print(f"Tarefas no banco: {cursor.fetchone()[0]}")
```

### 9.3 Verificar Logs

```bash
# Logs do Django
tail -f /var/log/saacb/django.log

# Logs Docker
docker logs saacb-django-teste -f

# Logs Gunicorn (no container)
docker exec saacb-django-teste cat /proc/1/fd/1
```

### 9.4 Verificar Status das APIs

**SISGRU:**
```python
from tarefas.gru.gru_service import SISGRUService

service = SISGRUService('usuario', 'senha', producao=False)
try:
    resultado = service.consultar_gru('10000000000123456789000000000000')
    print("✅ SISGRU OK")
except Exception as e:
    print(f"❌ SISGRU ERRO: {e}")
```

**API de Cálculos:**
```python
from tarefas.integracao.calculadora_client import CalculadoraClient

client = CalculadoraClient()
if client.ping():
    print("✅ API Cálculos OK")
else:
    print("❌ API Cálculos OFFLINE")
```

### 9.5 Verificar Static Files

```bash
# Verificar se static files existem
ls -la static/

# Verificar se foram coletadas
ls -la staticfiles/

# Verificar permissões
ls -la static/css/
```

### 9.6 Verificar Templates

```bash
# Verificar se template existe
find . -name "calcular_creditos.html"

# Verificar permissões
ls -la tarefas/templates/tarefas/integracao/
```

### 9.7 Verificar Configurações

```python
# Django shell
python manage.py shell

from django.conf import settings

print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"DATABASE: {settings.DATABASES}")
print(f"SISGRU_USUARIO: {settings.SISGRU_USUARIO}")
print(f"SISGRU_PRODUCAO: {settings.SISGRU_PRODUCAO}")
print(f"CALCULADORA_API_URL: {settings.CALCULADORA_API_URL}")
```

### 9.8 Verificar Usuários e Permissões

```python
# Django shell
python manage.py shell

from django.contrib.auth.models import User

users = User.objects.all()
for u in users:
    print(f"User: {u.username}, Active: {u.is_active}, Staff: {u.is_staff}")

# Verificar tarefas por usuário
from tarefas.models import tarefassamc

for user in users:
    count = tarefassamc.objects.filter(assigned_user=user).count()
    print(f"{user.username}: {count} tarefas")
```

### 9.9 Verificar Integrations

```bash
# Verificar se módulo pode ser importado
python -c "from tarefas.integracao import CalculadoraClient; print('✅ OK')"

# Verificar se gru_service pode ser importado
python -c "from tarefas.gru.gru_service import SISGRUService; print('✅ OK')"

# Verificar se services pode ser importado
python -c "from tarefas.services import gerar_texto_documento; print('✅ OK')"
```

---

## 10. COMANDOS ÚTEIS

### 10.1 Gerenciamento do Projeto

```bash
# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor de desenvolvimento
python manage.py runserver

# Shell interativo Django
python manage.py shell

# Testar aplicação
python manage.py test

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Aplicar migrations
python manage.py migrate

# Criar nova migration
python manage.py makemigrations

# Mostrar migrations
python manage.py showmigrations

# Verificar configuração
python manage.py check --deploy
```

### 10.2 Comandos Docker

```bash
# Subir containers
docker-compose up -d

# Subir com perfil de produção
docker-compose --profile production up -d

# Ver logs
docker-compose logs -f saacb

# Parar containers
docker-compose down

# Reconstruir imagem
docker-compose build --no-cache

# Executar comando no container
docker exec -it saacb-django-teste python manage.py shell

# Copiar arquivo para container
docker cp arquivo.txt saacb-django-teste:/app/

# Copiar arquivo do container
docker cp saacb-django-teste:/app/arquivo.txt ./

# Ver containers rodando
docker ps

# Ver todos os containers
docker ps -a
```

### 10.3 Comandos de Diagnóstico

```bash
# Diagnóstico completo (script do projeto)
python diagnostico_completo.py

# Testar integração
python testar_integracao.py

# Verificar migrations
python fix-migrations.py

# Diagnóstico Django
python diagnostico_django.py
```

### 10.4 Comandos de Banco de Dados

```bash
# Backup SQLite
cp db.sqlite3 db.sqlite3.backup

# Restore SQLite
cp db.sqlite3.backup db.sqlite3

# Verificar tamanho do banco
ls -lh db.sqlite3

# Verificar tabelas
sqlite3 db.sqlite3 ".tables"

# Verificar schema de uma tabela
sqlite3 db.sqlite3 ".schema tarefas_tarefassamc"

# Contar registros
sqlite3 db.sqlite3 "SELECT COUNT(*) FROM tarefas_tarefassamc;"
```

### 10.5 Comandos de Git

```bash
# Status
git status

# Adicionar arquivos
git add .

# Commit
git commit -m "mensagem"

# Push
git push

# Pull
git pull

# Ver branches
git branch

# Criar branch
git checkout -b nova-feature

# Ver log
git log --oneline
```

---

## 11. RECURSOS DE REFERÊNCIA

### 11.1 Documentação do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `README.md` | Documentação principal |
| `STATUS.md` | Relatório de status do sistema |
| `DOCKER.md` | Guia completo Docker |
| `RESUMO_IMPLEMENTACAO.md` | Resumo da implementação de integração |
| `RESUMO_CORRECOES.md` | Histórico de correções |
| `GUIA_CALCULOS.md` | Guia funcionalidade de cálculos |
| `GUIA_SISGRU.md` | Guia integração SISGRU |
| `docs/DESIGN-SYSTEM.md` | Documentação Design System |

### 11.2 Scripts Úteis

| Script | Descrição |
|--------|-----------|
| `diagnostico_completo.py` | Diagnóstico completo do sistema |
| `testar_integracao.py` | Teste de integração |
| `fix-migrations.py` | Corrigir migrations manualmente |
| `diagnostico_django.py` | Diagnóstico Django |

### 11.3 Documentação Externa

| Recurso | URL |
|---------|-----|
| Django 4.2 | https://docs.djangoproject.com/en/4.2/ |
| Django REST Framework | https://www.django-rest-framework.org/ |
| Bootstrap 5 | https://getbootstrap.com/ |
| WhiteNoise | https://whitenoise.evans.io/ |
| SISGRU API | https://www.gov.br/conecta/catalogo/apis/sisgru-guia-de-recolhimento-da-uniao |
| FastAPI | https://fastapi.tiangolo.com/ |

### 11.4 Variáveis de Ambiente (.env)

```bash
# Django
DEBUG=True
SECRET_KEY=django-insecure-chave-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
PORT=30010

# Database
DATABASE_URL=sqlite:////app/data/db.sqlite3

# SISGRU
SISGRU_USUARIO=seu_usuario
SISGRU_SENHA=sua_senha
SISGRU_PRODUCAO=False

# API Cálculos
CALCULADORA_API_URL=http://192.168.1.51:8002
CALCULADORA_API_TOKEN=

# Ollama (opcional)
OLLAMA_HOST=http://192.168.1.51:11434
OLLAMA_MODEL=llama3:8b
```

### 11.5 Configuração Django Importante

```python
# settings.py

# DEBUG
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback')

# ALLOWED_HOSTS
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = [
    'https://saacb.lakeserver.online',
    'http://saacb.lakeserver.online',
    'http://localhost:30010',
    'http://192.168.1.51:30010',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static/Media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# SISGRU
SISGRU_USUARIO = os.environ.get('SISGRU_USUARIO')
SISGRU_SENHA = os.environ.get('SISGRU_SENHA')
SISGRU_PRODUCAO = os.environ.get('SISGRU_PRODUCAO', 'False') == 'True'
GRU_PDF_DIR = os.path.join(BASE_DIR, 'media', 'gru_pdfs')

# Timezone
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Login
LOGIN_URL = '/admin/login/'
```

---

## 📝 CHECKLIST RÁPIDO PARA DEBUG

Quando um bug é reportado, seguir este checklist:

- [ ] 1. Reproduzir o erro (anotar passo a passo)
- [ ] 2. Verificar logs do Django/Gunicorn
- [ ] 3. Verificar logs do browser (console JavaScript)
- [ ] 4. Verificar se migrations estão aplicadas (`showmigrations`)
- [ ] 5. Verificar status das APIs externas (ping)
- [ ] 6. Verificar configuração de `.env`
- [ ] 7. Verificar permissões de arquivos/templates
- [ ] 8. Verificar se static files foram coletadas
- [ ] 9. Verificar se middleware está configurado corretamente
- [ ] 10. Rodar `python manage.py check --deploy`
- [ ] 11. Consultar este documento para erros conhecidos
- [ ] 12. Se necessário, rodar `diagnostico_completo.py`

---

## 🎯 CONCLUSÃO

Este documento fornece um mapa completo do sistema SAACB, incluindo:

- ✅ Estrutura de arquivos e diretórios
- ✅ Modelos de dados e suas relações
- ✅ URLs e rotas disponíveis
- ✅ Integrações externas e seus endpoints
- ✅ Fluxos de trabalho principais
- ✅ Erros conhecidos e soluções
- ✅ Comandos úteis para diagnóstico
- ✅ Pontos de atenção para debug

**Para uma IA ajudar com a solução de bugs:**

1. Comece lendo a seção de **[Erros Conhecidos e Soluções](#8-erros-conhecidos-e-soluções)**
2. Se o erro não estiver listado, siga o **[Checklist Rápido para Debug](#-checklist-rápido-para-debug)**
3. Consulte as seções relevantes baseadas no componente afetado
4. Use os comandos em **[Comandos Úteis](#10-comandos-úteis)** para diagnóstico

---

**Versão:** 1.0  
**Data:** 2026-03-21  
**Autor:** PITT (Code-AI Assistant)  
**Projeto:** SAACB - Sistema de Análises e Gestão de GRUs  
**Status:** ✅ Documentação Completa
