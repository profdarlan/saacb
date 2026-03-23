# 🔗 GUIA COMPLETO: INTEGRAÇÃO SISGRU NO SAACB

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Uso](#uso)
5. [Exemplos](#exemplos)
6. [Troubleshooting](#troubleshooting)
7. [API Reference](#api-reference)

---

## <a name="visão-geral"></a>1. VISÃO GERAL

### O que é GRU?
**Guia de Recolhimento da União** - Instrumento de recolhimento de receitas devidas à União, utilizado para recolhimento de multas, taxas, etc.

### O que é SISGRU?
**Sistema de Gestão de Recolhimento da União** - API do Governo Federal que permite:
- ✅ Consultar dados de GRUs existentes
- ✅ Validar GRUs
- ✅ Rastrear pagamentos
- ✅ Retificar dados
- ✅ Solicitar restituições

### Integração no SAACB
A funcionalidade permite que a SAACB:
1. Consulte GRUs já geradas no governo
2. Valide números de GRU
3. Rastreie status de pagamento
4. Gere PDFs visuais das GRUs
5. Integre dados com o banco de dados local

---

## <a name="instalação"></a>2. INSTALAÇÃO

### Passo 1: Instalar Dependências

```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instalar pacotes necessários
pip install requests==2.31.0
pip install reportlab==4.0.7
```

### Passo 2: Adicionar Arquivos ao Projeto

```
projeto-saacb/
└── tarefas/
    ├── gru/                          # NOVA PASTA
    │   ├── __init__.py
    │   ├── views.py                  # Views para GRU
    │   ├── urls.py                   # Rotas para GRU
    │   ├── forms.py                  # Formulários
    │   ├── models.py                 # Modelo GRU (opcional)
    │   ├── gru_service.py            # Serviço SISGRU
    │   ├── templates/
    │   │   ├── gru_form.html
    │   │   ├── gru_resultado.html
    │   │   └── gru_pdf.html
    │   └── tests.py
```

### Passo 3: Criar Pastas e Arquivos

```bash
# Linux/Mac
mkdir -p tarefas/gru/templates/gru

# Criar arquivos vazios
touch tarefas/gru/__init__.py
touch tarefas/gru/views.py
touch tarefas/gru/urls.py
touch tarefas/gru/forms.py
touch tarefas/gru/models.py
touch tarefas/gru/tests.py
```

### Passo 4: Atualizar URLs Principais

**arquivo: `projeto_saacb/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tarefas/', include('tarefas.urls')),
    path('gru/', include('tarefas.gru.urls')),  # 👈 ADICIONAR ESTA LINHA
]
```

---

## <a name="configuração"></a>3. CONFIGURAÇÃO

### Passo 1: Adicionar Credenciais em Settings

**arquivo: `projeto_saacb/settings.py`**

```python
# ============ CONFIGURAÇÃO SISGRU ============

# Conecta.Gov.BR Credentials
SISGRU_USUARIO = os.environ.get('SISGRU_USUARIO', 'seu_usuario')
SISGRU_SENHA = os.environ.get('SISGRU_SENHA', 'sua_senha')
SISGRU_PRODUCAO = os.environ.get('SISGRU_PRODUCAO', 'False') == 'True'

# Caminho para armazenar PDFs gerados
GRU_PDF_DIR = os.path.join(BASE_DIR, 'media', 'gru_pdfs')

# Garantir que o diretório existe
os.makedirs(GRU_PDF_DIR, exist_ok=True)

# Timeout para requisições (em segundos)
GRU_REQUEST_TIMEOUT = 30

# Habilitar cache de GRUs (em minutos)
GRU_CACHE_TIMEOUT = 60
```

### Passo 2: Configurar Variáveis de Ambiente

**arquivo: `.env` (criar na raiz do projeto)**

```bash
# ============ SISGRU API ============
SISGRU_USUARIO=seu_usuario_conecta
SISGRU_SENHA=sua_senha_conecta
SISGRU_PRODUCAO=False  # Use False para testes, True para produção
```

### Passo 3: Adicionar Aplicação (Opcional)

Se criar um app separado:

**arquivo: `projeto_saacb/settings.py`**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tarefas',
    'tarefas.gru',  # 👈 ADICIONAR
]
```

---

## <a name="uso"></a>4. USO

### Uso Básico - Serviço SISGRU

```python
from tarefas.gru.gru_service import SISGRUService, GRUPDFGenerator

# 1. Inicializar serviço
service = SISGRUService(
    usuario='seu_usuario',
    senha='sua_senha',
    producao=False  # False = homologação, True = produção
)

# 2. Consultar uma GRU
try:
    resultado = service.consultar_gru('10000000000123456789000000000000')
    
    # 3. Extrair dados estruturados
    dados = service.extrair_dados_gru(resultado)
    
    print(f"Valor: R$ {dados['valor']:,.2f}")
    print(f"Status: {dados['status']}")
    
    # 4. Gerar PDF
    generator = GRUPDFGenerator()
    generator.gerar_pdf(dados, '/tmp/gru.pdf')
    
except Exception as e:
    print(f"Erro: {e}")
```

### Uso em Views Django

```python
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .gru_service import SISGRUService, GRUPDFGenerator
from .forms import ConsultarGRUForm

class ConsultarGRUView(LoginRequiredMixin, View):
    template_name = 'gru/consultar.html'
    
    def get(self, request):
        form = ConsultarGRUForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ConsultarGRUForm(request.POST)
        
        if form.is_valid():
            try:
                # Inicializar serviço
                service = SISGRUService(
                    usuario=form.cleaned_data['usuario_sisgru'],
                    senha=form.cleaned_data['senha_sisgru'],
                    producao=form.cleaned_data['usar_producao']
                )
                
                # Consultar GRU
                resultado = service.consultar_gru(
                    form.cleaned_data['numero_gru']
                )
                
                # Extrair dados
                dados = service.extrair_dados_gru(resultado)
                
                # Gerar PDF se solicitado
                if form.cleaned_data['gerar_pdf']:
                    generator = GRUPDFGenerator()
                    arquivo_pdf = generator.gerar_pdf(dados)
                    dados['pdf_path'] = arquivo_pdf
                
                return render(request, 'gru/resultado.html', {
                    'dados': dados,
                    'sucesso': True
                })
                
            except Exception as e:
                return render(request, self.template_name, {
                    'form': form,
                    'erro': str(e),
                    'sucesso': False
                })
        
        return render(request, self.template_name, {'form': form})
```

---

## <a name="exemplos"></a>5. EXEMPLOS PRÁTICOS

### Exemplo 1: Validação de GRU

```python
from tarefas.gru.gru_service import SISGRUService

service = SISGRUService('usuario', 'senha')

# Validar um número
gru = '10000000000123456789000000000000'
if service.validar_numero_gru(gru):
    print("✓ Número válido")
else:
    print("✗ Número inválido")
```

### Exemplo 2: Consultar e Salvar no Banco

```python
from tarefas.gru.gru_service import SISGRUService
from tarefas.gru.models import GRU  # Se criar modelo

service = SISGRUService('usuario', 'senha')
resultado = service.consultar_gru('10000000000123456789000000000000')
dados = service.extrair_dados_gru(resultado)

# Salvar no banco
gru_obj = GRU.objects.create(
    numero=dados['numero_gru'],
    valor=dados['valor'],
    valor_recolhido=dados['valor_recolhido'],
    status=dados['status'],
    data_vencimento=dados['data_vencimento'],
    data_pagamento=dados['data_pagamento'],
)
```

### Exemplo 3: Listar Histórico de Movimentações

```python
service = SISGRUService('usuario', 'senha')
resultado = service.consultar_gru('numero_da_gru')
dados = service.extrair_dados_gru(resultado)

print("=== HISTÓRICO DE MOVIMENTAÇÕES ===")
for evento in dados['historia']:
    print(f"📅 {evento['data']}")
    print(f"📌 {evento['tipo']}: {evento['descricao']}")
    print()
```

### Exemplo 4: Integrar com Tarefa SAACB

```python
# Adicione este método ao model tarefassamc

class tarefassamc(models.Model):
    # ... campos existentes ...
    numero_gru = models.CharField(max_length=32, blank=True, null=True)
    
    def consultar_gru(self, usuario, senha):
        """Consulta a GRU associada a esta tarefa"""
        from tarefas.gru.gru_service import SISGRUService
        
        if not self.numero_gru:
            raise ValueError("Esta tarefa não tem GRU associada")
        
        service = SISGRUService(usuario, senha)
        resultado = service.consultar_gru(self.numero_gru)
        return service.extrair_dados_gru(resultado)
    
    def atualizar_status_gru(self, usuario, senha):
        """Atualiza o status baseado na GRU"""
        dados = self.consultar_gru(usuario, senha)
        
        if dados['status'] == 'PAGO':
            self.status = 'CONCLUÍDA'
            self.data_conclusao = dados['data_pagamento']
            self.save()
```

---

## <a name="troubleshooting"></a>6. TROUBLESHOOTING

### ❌ Erro: "Autenticação falhou"

**Causa:** Credenciais incorretas

**Solução:**
```bash
# 1. Verificar credenciais no .env
cat .env

# 2. Testar credenciais manualmente
python manage.py shell
>>> from tarefas.gru.gru_service import SISGRUService
>>> service = SISGRUService('seu_usuario', 'sua_senha')
>>> service.verificar_disponibilidade()
True
```

### ❌ Erro: "API indisponível"

**Causa:** API fora do horário de funcionamento (seg-sex 08:00-22:00)

**Solução:**
```python
from datetime import datetime
import pytz

# Verificar horário de Brasília
tz = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(tz)

if agora.weekday() < 5 and 8 <= agora.hour < 22:
    print("✓ API disponível")
else:
    print("✗ API indisponível - tente depois das 08:00 em dia útil")
```

### ❌ Erro: "GRU não encontrada"

**Causa:** Número de GRU inválido ou não existe

**Solução:**
```python
# Validar formato
service = SISGRUService('usuario', 'senha')
numero = '10000000000123456789000000000000'

if service.validar_numero_gru(numero):
    print("✓ Formato válido")
    # Se ainda não encontrar, número pode não existir
else:
    print("✗ Formato inválido")
```

### ❌ Erro: "ReportLab não está instalado"

**Solução:**
```bash
pip install reportlab==4.0.7
```

### ❌ Erro: "Timeout na requisição"

**Solução:**
```python
# Aumentar timeout em settings.py
GRU_REQUEST_TIMEOUT = 60  # Aumentado para 60 segundos
```

---

## <a name="api-reference"></a>7. API REFERENCE

### SISGRUService

#### `__init__(usuario, senha, producao=False)`
Inicializa o serviço.

**Parâmetros:**
- `usuario` (str): Usuário Conecta.Gov.BR
- `senha` (str): Senha Conecta.Gov.BR
- `producao` (bool): False=homolog, True=produção

**Exemplo:**
```python
service = SISGRUService('usuario', 'senha', producao=False)
```

#### `consultar_gru(numero_gru)`
Consulta uma GRU na API.

**Parâmetros:**
- `numero_gru` (str): Número com 32 dígitos

**Retorna:**
- dict: Resposta bruta da API

**Exceções:**
- `SISGRUAPIError`: Erro na requisição

**Exemplo:**
```python
resultado = service.consultar_gru('10000000000123456789000000000000')
```

#### `validar_numero_gru(numero_gru)`
Valida o formato de uma GRU.

**Parâmetros:**
- `numero_gru` (str): Número a validar

**Retorna:**
- bool: True se válido

**Exemplo:**
```python
if service.validar_numero_gru(numero):
    print("✓ Válido")
```

#### `extrair_dados_gru(dados_brutos)`
Extrai dados estruturados da resposta.

**Parâmetros:**
- `dados_brutos` (dict): Resposta da API

**Retorna:**
- dict: Dados estruturados com chaves:
  - `numero_gru`
  - `valor`
  - `valor_recolhido`
  - `data_vencimento`
  - `data_pagamento`
  - `status`
  - `historia`

**Exemplo:**
```python
dados = service.extrair_dados_gru(resultado)
print(dados['valor'])
```

#### `verificar_disponibilidade()`
Verifica se API está disponível.

**Retorna:**
- bool: True se disponível

**Exemplo:**
```python
if service.verificar_disponibilidade():
    print("✓ API disponível")
```

### GRUPDFGenerator

#### `gerar_pdf(dados_gru, arquivo_saida=None)`
Gera PDF visual da GRU.

**Parâmetros:**
- `dados_gru` (dict): Dados estruturados da GRU
- `arquivo_saida` (str): Caminho do arquivo (opcional)

**Retorna:**
- str: Caminho do arquivo gerado

**Exceções:**
- `SISGRUAPIError`: Erro ao gerar PDF

**Exemplo:**
```python
generator = GRUPDFGenerator()
arquivo = generator.gerar_pdf(dados, '/tmp/gru.pdf')
```

---

## 📚 Recursos Adicionais

### Documentação Oficial
- 🔗 [Catálogo de APIs - SISGRU](https://www.gov.br/conecta/catalogo/apis/sisgru-guia-de-recolhimento-da-uniao)
- 📖 [Documentação Técnica SISGRU](https://webservice.sisgru.tesouro.gov.br/sisgru/services/v1/docs/sisgru_ws_specs.html)
- 🎓 [Conecta.Gov.BR](https://www.gov.br/conecta/)

### Bibliotecas Utilizadas
- 📦 [Requests](https://docs.python-requests.org/) - Requisições HTTP
- 📦 [ReportLab](https://www.reportlab.com/) - Geração de PDFs
- 📦 [Django](https://docs.djangoproject.com/) - Framework web

### Contato de Suporte
- **FAQs:** https://www.gov.br/governodigital/pt-br/infraestrutura-nacional-de-dados/interoperabilidade/conecta-gov.br/acessar-os-servicos-do-conecta
- **Horário de funcionamento:** Seg-sex, 08:00-22:00 (Brasília)

---

## ✅ Checklist de Implementação

- [ ] Instalar dependências (requests, reportlab)
- [ ] Criar estrutura de pastas
- [ ] Copiar arquivos (gru_service.py, gru_forms.py)
- [ ] Criar views.py e urls.py
- [ ] Adicionar credenciais ao .env
- [ ] Atualizar settings.py
- [ ] Atualizar urls principais
- [ ] Criar templates HTML
- [ ] Testar em homologação
- [ ] Migrar para produção

---

**Criado em:** 2025-12-31  
**Versão:** 1.0.0  
**Status:** ✅ Pronto para uso
