# 📚 Documentação Completa - Sistema SAACB

**Sistema de Análises e Gestão de GRUs SAACB**

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Instalação](#instalação)
4. [Configuração](#configuração)
5. [Aplicações](#aplicações)
6. [Modelos de Dados](#modelos-de-dados)
7. [Integrações](#integrações)
8. [APIs](#apis)
9. [Design System](#design-system)
10. [Deploy](#deploy)
11. [Troubleshooting](#troubleshooting)

---

## <a name="visão-geral"></a>1. VISÃO GERAL

### O que é SAACB?

Sistema de **Análises e Gestão de GRUs** para o INSS, permitindo:

- ✅ Gestão completa de tarefas de análise
- ✅ Controle de GRUs (Guia de Recolhimento da União)
- ✅ Integração com SISGRU (API do Governo)
- ✅ Integração com API de Cálculos de Créditos
- ✅ Geração automática de relatórios e PDFs
- ✅ Interface baseada em Django Admin
- ✅ Design System customizado (identidade INSS)

### Tecnologias

| Componente | Tecnologia |
|-----------|-----------|
| Backend | Django 4.2.7 |
| Banco de Dados | SQLite |
| Frontend | Bootstrap 5 + Design System |
| API Externa | SISGRU (Governo Federal) |
| Cálculos | FastAPI (planilha_saacb) |
| Deploy | Docker + Gunicorn |

---

## <a name="docker"></a>DOCKER

### Deploy Rápido com Docker

Para fazer o deploy do sistema usando Docker:

```bash
# 1. Configurar variáveis de ambiente
cp .env.example .env
nano .env

# 2. Subir container
docker-compose up -d

# 3. Ver logs
docker-compose logs -f saacb

# 4. Acessar
# Sistema: http://localhost:30010
# Admin: http://localhost:30010/admin/
```

### Corrigir Erro de Migrations

Se aparecer o erro `no such column: tarefas_tarefassamc.valor_original_calculado`:

```bash
# Opção 1: Executar script de correção
docker exec -it saacb-app python fix-migrations.py

# Opção 2: Aplicar migrations manualmente
docker exec -it saacb-app python manage.py migrate

# Opção 3: Recriar container com correções
./fix-docker.sh
```

### Documentação Completa Docker

Veja [DOCKER.md](DOCKER.md) para:
- Guia completo de deploy
- Troubleshooting
- Boas práticas
- Configuração de produção

---

## <a name="arquitetura"></a>2. ARQUITETURA

### Estrutura do Projeto

```
projeto-saacb/
├── projeto_saacb/           # Configuração do Django
│   ├── __init__.py
│   ├── settings.py          # Configurações principais
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
│   │   └── calculadora_client.py
│   ├── views_integracao.py # Views de integração
│   └── templates/         # Templates HTML
│
├── static/                 # Arquivos estáticos
│   └── css/
│
├── media/                  # Uploads (PDFs, etc.)
│   └── gru_pdfs/
│
├── templates/              # Templates globais
│   ├── base.html
│   └── design-system/     # Componentes do DS
│
├── docs/                  # Documentação
│   ├── DESIGN-SYSTEM.md
│   └── README.md
│
├── manage.py              # CLI Django
├── requirements.txt        # Dependências
└── .env                   # Variáveis de ambiente
```

### Fluxo de Dados

```
┌─────────────┐
│   Django    │
│    Admin    │
└──────┬──────┘
       │
       ├─────────────┬──────────────┐
       │             │              │
       ▼             ▼              ▼
  ┌─────────┐  ┌─────────┐  ┌─────────────┐
  │ Tarefas │  │  GRUs   │  │ Integração  │
  └────┬────┘  └────┬────┘  └──────┬──────┘
       │            │              │
       ▼            ▼              ▼
  ┌─────────┐  ┌─────────┐  ┌─────────────┐
  │SQLite DB │  │SISGRU   │  │Planilha    │
  └─────────┘  │API Gov. │  │Cálculos API│
              └─────────┘  └─────────────┘
```

---

## <a name="instalação"></a>3. INSTALAÇÃO

### Requisitos

- Python 3.11+
- pip
- Virtualenv (recomendado)

### Passo 1: Clonar o Repositório

```bash
git clone <repo-url>
cd projeto-saacb
```

### Passo 2: Criar Ambiente Virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Variáveis de Ambiente

```bash
cp .env.example .env
# Editar .env com suas configurações
```

### Passo 5: Executar Migrations

```bash
python manage.py migrate
```

### Passo 6: Criar Superusuário

```bash
python manage.py createsuperuser
```

### Passo 7: Executar Servidor

```bash
python manage.py runserver
```

Acesse: http://localhost:8000/admin/

---

## <a name="configuração"></a>4. CONFIGURAÇÃO

### Variáveis de Ambiente (.env)

```bash
# Django
DEBUG=True
SECRET_KEY=sua_chave_secreta
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (opcional, usa SQLite por padrão)
DATABASE_URL=sqlite:///app/data/db.sqlite3

# SISGRU (API do Governo)
SISGRU_USUARIO=seu_usuario_conecta
SISGRU_SENHA=sua_senha_conecta
SISGRU_PRODUCAO=False

# API de Cálculos
CALCULADORA_API_URL=http://192.168.1.51:8002
CALCULADORA_API_TOKEN=seu_token_aqui

# Ollama (para automação - opcional)
OLLAMA_HOST=http://192.168.1.51:11434
OLLAMA_MODEL=llama3:8b
```

### Configurações Django (settings.py)

#### Debug e Segurança

```python
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
```

#### Banco de Dados

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Arquivos Estáticos e Media

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

#### Configuração SISGRU

```python
# Conecta.Gov.BR Credentials
SISGRU_USUARIO = os.environ.get('SISGRU_USUARIO', 'seu_usuario')
SISGRU_SENHA = os.environ.get('SISGRU_SENHA', 'sua_senha')
SISGRU_PRODUCAO = os.environ.get('SISGRU_PRODUCAO', 'False') == 'True'

# Caminho para PDFs
GRU_PDF_DIR = os.path.join(BASE_DIR, 'media', 'gru_pdfs')
os.makedirs(GRU_PDF_DIR, exist_ok=True)
```

---

## <a name="aplicações"></a>5. APLICAÇÕES

### Aplicação Principal: `tarefas`

Gerencia todas as funcionalidades do sistema.

#### Módulos

1. **Tarefas** - Gestão de análises
2. **GRUs** - Guia de Recolhimento da União
3. **Integração** - Conexão com API de cálculos

#### URLs Disponíveis

| Path | Descrição |
|------|-----------|
| `/` | Redirect para `/tarefas/` |
| `/admin/` | Django Admin |
| `/tarefas/` | Lista de tarefas |
| `/tarefas/<id>/` | Detalhes da tarefa |
| `/tarefas/create/` | Criar nova tarefa |
| `/tarefas/<id>/update/` | Editar tarefa |
| `/gru/` | Consulta de GRUs |
| `/tarefas/tarefa/<id>/calcular/` | Calcular créditos |
| `/tarefas/tarefa/<id>/pdf/` | Baixar PDF de cálculo |
| `/tarefas/tarefa/<id>/excel/` | Baixar Excel de cálculo |

---

## <a name="modelos-de-dados"></a>6. MODELOS DE DADOS

### 1. tarefassamc

Modelo principal para tarefas de análise.

**Campos Principais:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nome_interessado` | CharField | Nome do interessado |
| `CPF` | CharField | CPF |
| `tarefa_n` | CharField | Número da tarefa |
| `sei_n` | CharField | Número SEI |
| `servico` | CharField | Tipo de serviço |
| `nb1` | CharField | Benefício 1 |
| `nb2` | CharField | Benefício 2 |
| `valor` | CharField | Valor do débito |
| `status` | CharField | Status da análise |
| `assigned_user` | ForeignKey | Usuário responsável |

**Campos de Integração (cálculo de créditos):**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `valor_original_calculado` | DecimalField | Valor original calculado |
| `valor_corrigido_calculado` | DecimalField | Valor corrigido calculado |
| `valor_diferenca` | DecimalField | Diferença calculada |
| `detalhes_calculo` | JSONField | Detalhes do cálculo |
| `relatorio_pdf` | FileField | Relatório PDF |
| `calculado_em` | DateTimeField | Data do cálculo |

### 2. GRU

Modelo para GRUs consultadas/criadas.

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

### 3. Modelos de Apoio

#### `tipo_servico` - Tipos de serviços
#### `nome_motiv` - Motivos de ressarcimento
#### `conc_analise` - Conclusões de análise
#### `Role` - Funções de usuários
#### `UserProfile` - Perfil do usuário

---

## <a name="integrações"></a>7. INTEGRAÇÕES

### Integração 1: SISGRU (API Governo)

**Objetivo:** Consultar e validar GRUs no sistema do governo.

**Endpoint:** `https://webservice.sisgru.tesouro.gov.br`

**Funcionalidades:**
- Consultar GRU por número
- Validar número de GRU
- Extrair dados estruturados
- Gerar PDF visual
- Rastrear status de pagamento

**Arquivo:** `tarefas/gru/gru_service.py`

**Exemplo de Uso:**

```python
from tarefas.gru.gru_service import SISGRUService

service = SISGRUService('usuario', 'senha', producao=False)
resultado = service.consultar_gru('10000000000123456789000000000000')
dados = service.extrair_dados_gru(resultado)
```

**Documentação:** [GUIA_SISGRU.md](tarefas/gru/GUIA_SISGRU.md)

---

### Integração 2: API de Cálculos (Planilha SAACB)

**Objetivo:** Calcular correções monetárias automaticamente.

**Endpoint:** `http://192.168.1.51:8002`

**Funcionalidades:**
- Calcular créditos com índices
- Gerar Excel editável
- Gerar PDF de relatório
- Obter índices configurados

**Arquivo:** `tarefas/integracao/calculadora_client.py`

**Exemplo de Uso:**

```python
from tarefas.integracao import CalculadoraClient, tarefa_para_calculo

client = CalculadoraClient()
beneficiario, creditos = tarefa_para_calculo(tarefa)
indices = client.obter_indices_padrao()
resultado = client.calcular(beneficiario, creditos, indices)
```

**Documentação:** [RESUMO_INTEGRACAO.md](RESUMO_INTEGRACAO.md)

---

## <a name="apis"></a>8. APIs

### API Interna (Django)

Todas as APIs são acessíveis via Django Admin ou views customizadas.

#### Endpoints AJAX

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/tarefas/api/calcular/` | POST | Calcular créditos (AJAX) |
| `/tarefas/api/status/` | GET | Status da API de cálculos |

#### Exemplo de Uso (AJAX)

```javascript
fetch('/tarefas/api/calcular/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        tarefa_id: 123
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### API Externa: SISGRU

**Base URL:** `https://webservice.sisgru.tesouro.gov.br/sisgru/services/v1`

**Horário de funcionamento:** Seg-Sex, 08:00-22:00 (Brasília)

**Autenticação:** Conecta.Gov.BR

---

### API Externa: Planilha Cálculos

**Base URL:** `http://192.168.1.51:8002`

**Documentação:** [docs/API.md](../saacb-integracao/docs/API.md)

**Endpoints Principais:**

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/calcular` | POST | Calcular créditos |
| `/api/gerar-excel` | POST | Gerar Excel |
| `/api/gerar-relatorio-pdf` | POST | Gerar PDF |
| `/api/indices-padrao` | GET | Obter índices |
| `/api/upload-pdf` | POST | Upload e extração |

---

## <a name="design-system"></a>9. DESIGN SYSTEM

**Identidade Visual:** INSS

**Base:** Bootstrap 5 + CSS customizado

### Componentes Disponíveis

1. **Botões** - Primary, Success, Danger, Outline
2. **Cards** - Com e sem header
3. **Badges** - Status, informações
4. **Stat Cards** - Estatísticas
5. **Empty States** - Estados vazios

### Cores

```css
--ds-primary: #005696;      /* Azul INSS */
--ds-accent: #ffcc00;        /* Amarelo */
--ds-success: #28a745;
--ds-warning: #ffc107;
--ds-danger: #dc3545;
--ds-info: #17a2b8;
```

### Uso

```django
{% include "design-system/button.html" with text="Salvar" variant="primary" icon="check" %}
{% include "design-system/card.html" with title="Informações" icon="info-circle" %}
{% include "design-system/badge.html" with text="Pendente" variant="warning" %}
```

**Documentação:** [DESIGN-SYSTEM.md](docs/DESIGN-SYSTEM.md)

---

## <a name="deploy"></a>10. DEPLOY

### Opção 1: Docker

```bash
docker build -t saacb .
docker run -p 8000:8000 saacb
```

### Opção 2: Gunicorn

```bash
pip install gunicorn
gunicorn projeto_saacb.wsgi:application --bind 0.0.0.0:8000
```

### Opção 3: Systemd Service

**Arquivo:** `/etc/systemd/system/saacb.service`

```ini
[Unit]
Description=SAACB Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/projeto-saacb
Environment="PATH=/path/to/projeto-saacb/.venv/bin"
ExecStart=/path/to/projeto-saacb/.venv/bin/gunicorn projeto_saacb.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Ativar:**

```bash
sudo systemctl enable saacb
sudo systemctl start saacb
sudo systemctl status saacb
```

---

## <a name="troubleshooting"></a>11. TROUBLESHOOTING

### Erros Comuns

#### ❌ "No module named 'tarefas'"

**Causa:** Python path não configurado

**Solução:**
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/projeto-saacb"
# ou
python manage.py check
```

#### ❌ "Database locked"

**Causa:** SQLite não suporta concorrência alta

**Solução:** Usar PostgreSQL em produção

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'saacb',
        'USER': 'saacb',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### ❌ "SISGRU API indisponível"

**Causa:** Fora do horário de funcionamento

**Solução:** Verificar horário (Seg-Sex 08:00-22:00)

```python
from datetime import datetime
import pytz

tz = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(tz)
print(f"Hora atual (Brasília): {agora.hour:02d}:{agora.minute:02d}")
```

#### ❌ "API de cálculos não respondendo"

**Causa:** Servidor FastAPI não está rodando

**Solução:**
```bash
cd /path/to/planilha_saacb
uvicorn main:app --host 0.0.0.0 --port 8002
```

#### ❌ "Static files não encontradas"

**Causa:** STATIC_ROOT não configurado

**Solução:**
```bash
python manage.py collectstatic --noinput
```

---

### Logs

#### Django Logs

```bash
tail -f /var/log/saacb/django.log
```

#### API de Cálculos Logs

```bash
tail -f /tmp/planilha_server.log
```

---

### Comandos Úteis

#### Verificar Status do Projeto

```bash
python manage.py check --deploy
```

#### Listar Migrations

```bash
python manage.py showmigrations
```

#### Shell Django

```bash
python manage.py shell
```

#### Criar Superusuário

```bash
python manage.py createsuperuser
```

#### Backup SQLite

```bash
cp db.sqlite3 db.sqlite3.backup
```

---

## 📚 Recursos Adicionais

### Documentação Oficial

- [Django](https://docs.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [SISGRU API](https://www.gov.br/conecta/catalogo/apis/sisgru-guia-de-recolhimento-da-uniao)

### Documentação do Projeto

- [Design System](docs/DESIGN-SYSTEM.md)
- [Guia SISGRU](tarefas/gru/GUIA_SISGRU.md)
- [Resumo Integração](RESUMO_INTEGRACAO.md)

---

## 📝 Checklist de Manutenção

### Semanal

- [ ] Verificar logs de erros
- [ ] Backup do banco de dados
- [ ] Verificar espaço em disco

### Mensal

- [ ] Atualizar dependências
- [ ] Verificar segurança (Django check)
- [ ] Revisar usuários ativos

### Trimestral

- [ ] Audit de segurança
- [ ] Revisar integrações externas
- [ ] Atualizar documentação

---

**Versão:** 2.0.0
**Data:** 2025-03-19
**Status:** ✅ Produção
**Suporte:** Equipe de Desenvolvimento SAACB
