# 📊 Análise Completa - SAACB (Sistema de Análises e Gestão de GRUs)

**Data:** 2026-03-22
**Versão:** 2.0.0
**Status:** Produção (com bugs corrigidos)

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Aplicações](#aplicações)
4. [Modelos de Dados](#modelos-de-dados)
5. [Configurações](#configurações)
6. [Views e URLs](#views-e-urls)
7. [Templates](#templates)
8. [Integrações](#integrações)
9. [Deploy](#deploy)
10. [Bugs Corrigidos](#bugs-corrigidos)
11. [Próximos Passos](#proximos-passos)

---

## 🎯 Visão Geral

### O que é SAACB?

Sistema de **Análises e Gestão de GRUs** para o INSS, permitindo:

- ✅ Gestão completa de tarefas de análise administrativa
- ✅ Controle de GRUs (Guia de Recolhimento da União)
- ✅ Integração com SISGRU (API do Governo Federal)
- ✅ Integração com API de Cálculos de Créditos
- ✅ Geração automática de relatórios e PDFs
- ✅ Interface baseada em Django Admin customizado
- ✅ Dashboards analíticos
- ✅ Importação/Exportação de dados (Excel, CSV)

### Tecnologias

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| Backend | Django | 4.2.7 |
| Banco de Dados | SQLite | 3 |
| Servidor WSGI | Gunicorn | 22.0.0 |
| Frontend | Bootstrap 5 | 5.3.0 |
| PDF | ReportLab | 4.4.7 |
| Excel | pandas/openpyxl | 2.2.3/3.1.5 |
| Deploy | Docker + Docker Compose | - |

---

## 📁 Estrutura do Projeto

```
projeto-saacb/
├── projeto_saacb/           # Configurações do Django
│   ├── __init__.py
│   ├── settings.py          # Configurações principais
│   ├── settings_clean.py   # Configurações de desenvolvimento
│   ├── settings_prod.py     # Configurações de produção
│   ├── urls.py             # Rotas principais
│   └── wsgi.py             # WSGI para deploy
│
├── tarefas/                 # Aplicação principal
│   ├── models.py           # Modelos de dados
│   ├── views.py            # Views (CBVs + FBVs)
│   ├── admin.py            # Configuração do Admin
│   ├── urls.py             # Rotas de tarefas
│   ├── forms.py            # Formulários
│   ├── services.py         # Lógica de negócio
│   ├── gru/                # Módulo GRU
│   │   ├── gru_service.py  # Serviço SISGRU
│   │   ├── views.py        # Views GRU
│   │   └── urls.py         # Rotas GRU
│   ├── integracao/         # Integração com calculadora
│   │   ├── calculadora_client.py
│   │   └── views_integracao.py
│   ├── templates/         # Templates HTML
│   ├── utils.py           # Utilitários (PDF, etc.)
│   └── signals.py          # Signals Django
│
├── dashboards/              # Aplicação de dashboards
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── gru/                     # Aplicação de GRUs (legado)
│   └── templates/
│
├── templates/              # Templates globais
│   ├── base.html          # Template base
│   ├── admin_login.html    # Login customizado
│   ├── design-system/     # Componentes do DS
│   ├── admin/             # Templates admin customizados
│   ├── dashboards/        # Templates dashboards
│   ├── grus/              # Templates GRUs
│   └── tarefas/           # Templates tarefas
│
├── static/                 # Arquivos estáticos
│   ├── css/
│   │   ├── style.css       # CSS customizado
│   │   └── design-system.css
│   └── admin/
│
├── media/                  # Uploads (PDFs, Excel, etc.)
│   ├── gru_pdfs/
│   └── relatorios/
│
├── data/                   # Banco de dados SQLite
│   └── db.sqlite3
│
├── docs/                  # Documentação
│   ├── README.md
│   ├── DESIGN-SYSTEM.md
│   └── ...
│
├── scripts/               # Scripts de automação
│   ├── sync-casaos.sh      # Sincronização com CASAOS
│   └── ...
│
├── Dockerfile              # Imagem Docker
├── docker-compose.yml      # Orquestração de containers
├── requirements.txt        # Dependências Python
├── manage.py              # CLI Django
└── .env                   # Variáveis de ambiente
```

---

## 🎨 Aplicações

### 1. `tarefas` (Principal)

Gerencia todas as funcionalidades do sistema.

**Funcionalidades:**
- CRUD de tarefas de análise
- Gestão de status (PENDENTE, EM_ANALISE, CONCLUIDA_INTERMEDIARIA, CONCLUIDA_FINALIZADA)
- Filtros e busca
- Ordenação múltipla
- Paginação
- Integração com calculadora de créditos
- Geração de relatórios PDF
- Exportação Excel/CSV

**Módulos:**
- `models.py` - Modelos de dados
- `views.py` - Views (TarefaListView, TarefaDetailView, etc.)
- `services.py` - Lógica de negócio
- `gru/gru_service.py` - Integração SISGRU
- `integracao/calculadora_client.py` - API de cálculos

### 2. `dashboards`

Visualização de dados e estatísticas.

**Funcionalidades:**
- Dashboard SAMC
- Exportação CSV
- Estatísticas por usuário
- Gráficos e métricas

### 3. `gru`

Gestão de GRUs (legado, migrando para `tarefas`).

---

## 🗄️ Modelos de Dados

### Modelos Principais

#### `Role`

Funções de usuários no sistema.

```python
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
```

**Funções padrão:** ADMINISTRADOR, ANALISTA, GESTOR

#### `UserProfile`

Perfil extendido do usuário Django.

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
```

#### `tipo_servico`

Tipos de serviços disponíveis.

Exemplo: REVISAO, CUMPRIMENTO, RESSARCIMENTO, etc.

#### `nome_motiv`

Motivos de ressarcimento.

#### `conc_analise`

Conclusões possíveis da análise.

**Status:**
- `PROCEDENTE` - Procede
- `PARCIALMENTE PROCEDENTE` - Parcialmente procedente
- `IMPROCEDENTE` - Improcedente

#### `tarefassamc`

Modelo principal para tarefas de análise.

**Campos Principais:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nome_interessado` | CharField | Nome do interessado |
| `CPF` | CharField | CPF (20 caracteres) |
| `tarefa_n` | CharField | Número da tarefa |
| `tarefa_a` | CharField | Tarefa anterior |
| `sei_n` | CharField | Número SEI |
| `servico` | ForeignKey | Tipo de serviço |
| `nb1` | CharField | NB 1 (Benefício 1) |
| `nb2` | CharField | NB 2 (Benefício 2) |
| `valor` | CharField | Valor do débito |
| `status` | CharField | Status da análise |
| `fase_analise` | CharField | Fase da análise |
| `assigned_user` | ForeignKey | Usuário responsável |
| `data_atribuicao` | DateTimeField | Data de atribuição |
| `atualizado_em` | DateTimeField | Última atualização |
| `concluida_em` | DateField | Data de conclusão |

**Campos de Integração (cálculo de créditos):**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `valor_original_calculado` | DecimalField | Valor original calculado |
| `valor_corrigido_calculado` | DecimalField | Valor corrigido calculado |
| `valor_diferenca` | DecimalField | Diferença calculada |
| `detalhes_calculo` | JSONField | Detalhes do cálculo |
| `relatorio_pdf` | FileField | Relatório PDF |
| `calculado_em` | DateTimeField | Data do cálculo |

**Índices:**
- `assigned_user` - Para consultas rápidas por usuário
- `status` - Para filtros por status
- `atualizado_em` - Para ordenação

#### `GRU`

Modelo para GRUs consultadas/criadas via SISGRU.

**Campos:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `beneficiario_nome` | CharField | Nome do beneficiário |
| `beneficiario_cpf` | CharField | CPF do beneficiário |
| `codigo_recolhimento` | CharField | Código da GRU |
| `competencia` | DateField | Competência |
| `vencimento` | DateField | Data de vencimento |
| `valor` | DecimalField | Valor |
| `status` | CharField | Status |
| `pdf_file` | FileField | PDF da GRU |
| `criado_por` | ForeignKey | Usuário que criou |
| `criado_em` | DateTimeField | Data de criação |

---

## ⚙️ Configurações

### settings.py

**Configurações principais:**

```python
# Debug e Hosts
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.51']

# URLs de login customizadas
LOGIN_URL = "/admin-login/"
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = "/admin-login/"

# Banco de dados (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data/db.sqlite3',
    }
}

# Arquivos estáticos e media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### docker-compose.yml

**Serviços:**

1. **`saacb`** - Django + Gunicorn
   - Porta: 30010:8000
   - Workers: 3
   - Timeout: 180s
   - Volumes: data, media, static

2. **`planilha-calculos`** - API de cálculos (FastAPI)
   - Porta: 8002:8000
   - Contexto: `../planilha_saacb`

3. **`postgres`** - PostgreSQL (production)
   - Profile: `production`

---

## 🌐 Views e URLs

### Rotas Principais (urls.py)

```python
urlpatterns = [
    path('admin-login/', admin_login, name='admin-login'),
    path('admin/', admin.site.urls),
    path('', lambda r: render(r, 'tarefas/tarefa_list.html'), name='home'),
    path('tarefas/', include('tarefas.urls')),
    path('gru/', include('tarefas.gru.urls')),
    path('dashboards/', include('dashboards.urls')),
    path('api/calcular/', include('tarefas.views_integracao')),
]
```

### Views de Tarefas

| View | Template | Descrição |
|------|----------|-----------|
| `TarefaListView` | `tarefas/tarefa_list.html` | Lista de tarefas |
| `TarefaListOrdenadaView` | `tarefas/tarefa_list_moderna.html` | Lista moderna com ordenação |
| `TarefaDetailView` | `tarefas/tarefa_detail.html` | Detalhes da tarefa |
| `TarefaCreateView` | `tarefas/tarefa_form.html` | Criar nova tarefa |
| `TarefaUpdateView` | `tarefas/tarefa_form.html` | Editar tarefa |
| `TarefaDeleteView` | `tarefas/tarefa_confirm_delete.html` | Excluir tarefa |
| `TarefaCalcularView` | - | Calcular créditos (AJAX) |
| `TarefaPDFView` | - | Baixar PDF do cálculo |
| `TarefaExcelView` | - | Baixar Excel do cálculo |

### Views de Dashboards

| View | Template | Descrição |
|------|----------|-----------|
| `dashboard_samc` | `dashboards/dashboard_samc.html` | Dashboard principal |
| `exportar_csv_dashboard` | - | Exportar dados para CSV |

---

## 🎨 Templates

### Estrutura

```
templates/
├── base.html                  # Template base
├── admin_login.html           # Login customizado
├── design-system/            # Componentes do DS
│   ├── button.html
│   ├── card.html
│   └── ...
├── admin/                    # Templates admin (conflito removido)
├── dashboards/
│   └── dashboard_samc.html
├── grus/
│   └── ...
└── tarefas/                   # Templates de tarefas
    ├── tarefa_list.html
    ├── tarefa_list_moderna.html
    ├── tarefa_detail.html
    ├── tarefa_form.html
    └── tarefa_confirm_delete.html
```

### Templates Criados/Corrigidos

1. **`admin_login.html`** - Login customizado (fora de `admin/` para evitar conflito)
2. **`tarefas/tarefa_list.html`** - Lista simples com estatísticas
3. **`tarefas/tarefa_list_moderna.html`** - Lista moderna com paginação e ordenação
4. **`tarefas/tarefa_detail.html`** - Detalhes completos da tarefa
5. **`tarefas/tarefa_form.html`** - Formulário de criação/edição
6. **`tarefas/tarefa_confirm_delete.html`** - Confirmação de exclusão

---

## 🔌 Integrações

### 1. SISGRU (API Governo Federal)

**Objetivo:** Consultar e validar GRUs no sistema do governo.

**Arquivo:** `tarefas/gru/gru_service.py`

**Métodos:**
- `consultar_gru(codigo)` - Consulta GRU por código
- `validar_gru(codigo)` - Valida número de GRU
- `extrair_dados_gru(html)` - Extrai dados estruturados do HTML

### 2. API de Cálculos (Planilha SAACB)

**Objetivo:** Calcular correções monetárias automaticamente.

**Arquivo:** `tarefas/integracao/calculadora_client.py`

**Métodos:**
- `calcular(beneficiario, creditos, indices)` - Calcula créditos
- `obter_indices_padrao()` - Retorna índices configurados
- `gerar_relatorio_pdf(...)` - Gera PDF do relatório

---

## 🚀 Deploy

### Docker

**Construir imagem:**
```bash
docker build -t saacb .
```

**Subir container:**
```bash
docker-compose up -d
```

**Ver logs:**
```bash
docker-compose logs -f saacb
```

### Variáveis de Ambiente (.env)

```bash
# Django
DEBUG=True
SECRET_KEY=sua_chave_secreta
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.51

# Database
DATABASE_URL=sqlite:////app/data/db.sqlite3

# SISGRU
SISGRU_USUARIO=seu_usuario
SISGRU_SENHA=sua_senha
SISGRU_PRODUCAO=False

# API de Cálculos
CALCULADORA_API_URL=http://planilha-calculos:8000
CALCULADORA_API_TOKEN=seu_token
```

---

## 🐛 Bugs Corrigidos (Recentes)

### 1. TemplateDoesNotExist - admin/login
**Problema:** Template de login não encontrado.
**Solução:** Criado `templates/admin_login.html` fora do namespace `admin/`.

### 2. TemplateDoesNotExist - admin/index
**Problema:** Conflito de namespace `templates/admin/` com Django admin.
**Solução:** Movido templates para fora de `admin/` e criada rota customizada `/admin-login/`.

### 3. TemplateDoesNotExist - tarefas/
**Problema:** Templates de tarefas faltavam.
**Solução:** Criados todos os templates: `tarefa_list.html`, `tarefa_detail.html`, `tarefa_form.html`, etc.

### 4. ValueError - mail_admins handler
**Problema:** `DEFAULT_EXCEPTION_REPORTER` incompatível com Django 4.0+.
**Solução:** Removido do `settings.py`.

### 5. SystemCheckError - context processors
**Problema:** Context processors ausentes (auth, messages, request).
**Solução:** Adicionados na configuração de `TEMPLATES`.

### 6. ModuleNotFoundError - dashboards.models
**Problema:** Importação incorreta em `dashboards/views.py`.
**Solução:** Corrigido de `from .models` para `from tarefas.models`.

### 7. SyntaxError - settings.py
**Problema:** Aspas de fechamento faltando em `LOGIN_URL` e `LOGOUT_REDIRECT_URL`.
**Solução:** Adicionadas aspas de fechamento `"`.

---

## 📈 Banco de Dados

### Tamanho do Banco

```
-rw-r--r-- 1 node node  344064 bytes (Mar 22 21:47)
/data/.openclaw/workspace-dev/projeto-saacb/db.sqlite3
```

**Tamanho:** 344 KB (aprox. 300-400 registros estimados)

### Backups Disponíveis

- `db.sqlite3.backup-20260321.db` (274 KB)
- `db.sqlite3.old` (286 KB)

---

## 📝 Próximos Passos

### Imediatos

1. ✅ **Reiniciar container** no CASAOS para aplicar correções
2. ✅ **Criar superusuário** se não existir:
   ```bash
   docker exec -it saacb-django-teste python manage.py createsuperuser
   ```

### Curto Prazo

3. **Testar funcionalidades:**
   - Login no admin (`/admin-login/`)
   - Listagem de tarefas (`/tarefas/`)
   - Criação de nova tarefa
   - Edição de tarefa existente

4. **Validar integrações:**
   - API de cálculos respondendo?
   - SISGRU disponível?

5. **Melhorar dashboards:**
   - Adicionar gráficos de métricas
   - Exportar relatórios

### Médio Prazo

6. **Migração para PostgreSQL:**
   - SQLite para produção não é recomendado
   - Configurar Postgres via docker-compose

7. **Autenticação melhorada:**
   - Integração com LDAP/Active Directory
   - OAuth 2.0

8. **API REST:**
   - Expor dados via API para integrações externas
   - Documentação com Swagger/OpenAPI

### Longo Prazo

9. **Interface mobile:**
   - PWA ou app mobile
   - Responsividade aprimorada

10. **Testes automatizados:**
    - Testes unitários
    - Testes de integração
    - CI/CD

---

## 📞 Suporte

**Documentação:**
- `/docs/README.md`
- `/docs/DESIGN-SYSTEM.md`

**Scripts de automação:**
- `/scripts/sync-casaos.sh` - Sincroniza workspace-dev com CASAOS
- `/setup-docker.sh` - Configura ambiente Docker
- `/aplicar-migrations-docker.sh` - Aplica migrations no container

**Logs do container:**
```bash
docker logs saacb-django-teste --tail 50
```

---

**Análise concluída em:** 2026-03-22
**Estado do projeto:** ✅ Produção (com bugs corrigidos)
