# 📋 DASHBOARD SAMC - INTEGRAÇÃO COM SAACB

**Data:** 2026-03-21  
**Status:** ✅ CRIADO

---

## 📋 RESUMO

Dashboard SAMC é uma aplicação React com gráficos interativos que foi integrada ao sistema SAACB Django.

**Funcionalidades:**
- Visualizar dados do banco de dados (tabela tarefassamc)
- KPIs (Total, Pendentes, Concluídas, Atribuídas)
- Gráficos: Distribuição por status, Conclusões, Tipos de serviço
- Tabela de tarefas com ordenação e busca
- Exportar para CSV (admin: todas, usuário: só suas tarefas)
- Modal de detalhes da tarefa

---

## 📁 ESTRUTURA DE ARQUIVOS

```
projeto-saacb/
├── dashboards/                    # Novo app Django
│   ├── __init__.py             # Configuração do app
│   ├── views.py                 # Views Django
│   ├── urls.py                  # Rotas do app
│   └── templates/dashboards/
│       └── dashboard_samc.html  # Dashboard React (26KB)
├── projeto_saacb/
│   ├── settings.py               # INSTALLED_APPS atualizado
│   └── urls.py                   # URLs principais atualizadas
├── "Dashboard SAMC/"              # Original (pode ser removido)
│   └── ... (arquivos originais do dashboard)
```

---

## 🎨 FUNCIONALIDADES

### 1. Dashboard Principal
- **URL:** `/dashboards/dashboard-samc/`
- **Acesso:** Login requerido
- **Dados:** Tabela `tarefassamc` do Django

### 2. Permissões

| Perfil | O que pode ver/exportar |
|--------|-------------------------|
| **Administrador** (is_superuser) | Todas as tarefas (top 1000) |
| **Usuário Normal** | Só suas tarefas (assigned_user_id) |

**Nota:** Filtragem é automática baseada no usuário logado.

### 3. KPIs (Cards)

| Card | Descrição |
|------|-----------|
| 📊 Total de Tarefas | Total de registros visíveis |
| ⏳ Pendentes | Status = "PENDENTE" |
| ✅ Concluídas | Status contém "CONCLUÍDA" |
| 👥 Atribuídas | Tem assigned_user_id |

### 4. Gráficos

| Gráfico | Dados | Tipo |
|---------|-------|------|
| **Distribuição por Status** | Contagem por status | Pie Chart |
| **Conclusões** | Regular vs Irregular | Pie Chart |
| **Tipos de Serviço** | Top 6 por quantidade | Bar Chart |

### 5. Filtros

- **Busca:** Nome, CPF, Tarefa N, SEI N
- **Status:** Todos, Pendentes, Concluídas, Minhas (só usuário normal)

### 6. Ordenação

- **Clicar nos cabeçalhos** da tabela para ordenar
- **Colunas ordenáveis:** ID, Nome, CPF

### 7. Exportar CSV

- **Botão:** "Exportar CSV" com progresso
- **Admin:** Todas as tarefas
- **Usuário:** Só suas tarefas
- **Campos:** Todos os campos da tabela (30+)

### 8. Modal de Detalhes

- **Clicar em uma linha** para ver detalhes
- **Mostra:** Todos os campos da tarefa
- **Link:** "Editar no Admin" para acesso rápido

---

## 📊 CAMPOS EXPORTADOS (CSV)

| Campo | Descrição |
|-------|-----------|
| id | ID da tarefa |
| nome_interessado | Nome do interessado |
| CPF | CPF |
| tarefa_n | Número da tarefa |
| tarefa_a | Tarefa anterior |
| sei_n | Número SEI |
| procj | Processo judicial |
| servicos | Tipo de serviço |
| nome_serv_id | ID do nome de serviço |
| der_tarefa | Data do erro |
| nb1 | Benefício 1 |
| nb2 | Benefício 2 |
| sit_ben | Situação do benefício |
| aps | APS Manutenção |
| prazo | Prazo defesa |
| defesa_ap | Defesa apresentada |
| categoria | Categoria irregularidade |
| tip_con | Tipo de crédito |
| oficio1 | Ofício defesa (data) |
| oficio2 | Ofício recurso (data) |
| Competencia | Competência |
| data_irregular | Data início irregularidade |
| Periodo_irregular | Período irregular |
| valor | Valor |
| obs1 | Observação 1 |
| obs2 | Observação 2 |
| responsavel | Responsável |
| CPF_R | CPF do responsável |
| Conclusao | Conclusão |
| status | Status |
| historico | Histórico |
| servidor | Matrícula servidor |
| nome_tarefa_id | Nome usuário atribuído |
| assigned_user_id | ID usuário atribuído |
| AR1 | Ano Revisão 1 |
| AR2 | Ano Revisão 2 |
| env_serv | Envolvimento servidor |
| resp_credito | Responsável crédito |
| es_conc_id | ID conclusão análise |
| es_conc__conc | Descrição conclusão |
| data_def | Data defesa |
| data_rec | Data recurso |
| atualizado_em | Data atualização |
| concluida_em | Data conclusão |

**Total:** 30+ campos

---

## 🔧 CONFIGURAÇÃO

### 1. INSTALLED_APPS

**Arquivo:** `projeto_saacb/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tarefas.apps.TarefasConfig',
    'dashboards.apps.DashboardsConfig',  # ← ADICIONADO
]
```

### 2. URLs Principais

**Arquivo:** `projeto_saacb/urls.py`

```python
from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='/tarefas/'), name='home'),
    path('admin/', admin.site.urls),
    path('tarefas/', include('tarefas.urls')),
    path('gru/', include('tarefas.gru.urls')),
    path('dashboards/', include('dashboards.urls')),  # ← ADICIONADO
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 3. App Dashboards

**Arquivo:** `dashboards/apps.py`

```python
from django.apps import AppConfig

class DashboardsConfig(AppConfig):
    default_auto_field = '__all__'
    name = 'Dashboards (SAMC)'
    verbose_name = 'Dashboard SAMC'
```

---

## 📝 VIEWS DASHBOARD

**Arquivo:** `dashboards/views.py`

### Views Principais

| View | Descrição | Permissão |
|------|-----------|-----------|
| `dashboard_samc` | Renderiza dashboard com dados do banco | Login |
| `exportar_csv_dashboard` | Exporta tarefas para CSV | Login |

### Lógica de Permissões

```python
is_admin = request.user.is_superuser or request.user.groups.filter(name='Administrador').exists()

if is_admin:
    tarefas = tarefassamc.objects.all().order_by('-id')[:1000]
else:
    tarefas = tarefassamc.objects.filter(
        assigned_user_id=request.user.id
    ).order_by('-id')[:1000]
```

---

## 🎯 ROTAS

### Rota Dashboard

| Rota | View | Descrição |
|------|------|-----------|
| `/dashboards/dashboard-samc/` | `dashboard_samc` | Dashboard principal |

### Rota Exportar CSV

| Rota | View | Método | Descrição |
|------|------|---------|-----------|
| `/dashboards/exportar-csv/` | `exportar_csv_dashboard` | POST | Exporta dados em CSV |

### Namespaces

```python
# Em dashboards/urls.py
app_name = 'dashboards'

# URLs
path('dashboard-samc/', views.dashboard_samc, name='dashboard_samc'),
path('exportar-csv/', views.exportar_csv_dashboard, name='exportar_csv_dashboard'),
```

---

## 🚀 DEPLOY

### 1. Aplicar Migration

```bash
cd projeto-saacb
python manage.py makemigrations dashboards
python manage.py migrate
```

### 2. Coletar Static Files

```bash
python manage.py collectstatic --noinput
```

### 3. Reiniciar Docker

```bash
cd /DATA/AppData/fitt/projeto-saacb
docker restart saacb-django-teste
```

### 4. Acessar Dashboard

```
URL: http://192.168.1.51:30010/dashboards/dashboard-samc/
```

---

## 🎨 INTERFACE

### Cores

| Elemento | Cor | Hex |
|---------|-----|-----|
| Background | Navy | `#0f172a` |
| Card | Navy Dark | `#1e293b` |
| Border | Navy | `#334155` |
| Texto | White | `#e2e8f0` |
| Primary | Blue | `#3b82f6` |
| Success | Green | `#10b981` |
| Warning | Yellow | `#f59e0b` |
| Danger | Red | `#ef4444` |

### Tipografia

- **Fonte:** Inter (Google Fonts)
- **Pesos:** 300, 400, 500, 600, 700, 800
- **Títulos:** Bold (700/800)
- **Texto:** Regular (400/500)

---

## 📊 ESTATÍSTICAS

### Cálculos de KPIs

```python
stats = {
    'total': len(tarefas_list),
    'pendentes': len([t for t in tarefas_list if t['status'] == 'PENDENTE']),
    'concluidas': len([t for t in tarefas_list if 'CONCLUIDA' in t['status']]),
    'atribuidas': len([t for t in tarefas_list if t['assigned_user_id']]),
}
```

### Dados para Gráficos

```javascript
// Distribuição por status
const statusData = Object.entries(statusCounts).map(([status, count]) => ({
    name: status,
    value: count
}));

// Tipos de serviço (Top 6)
const servicoData = Object.entries(servicoCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6)
    .map(([servico, count]) => ({
        name: servico,
        value: count
    }));
```

---

## 🐛 ERROS CONHECIDOS

### 1. App Não Carrega

**Causa:** INSTALLED_APPS não atualizado

**Solução:**
```bash
python manage.py check
```

### 2. Template Not Found

**Causa:** Template na pasta errada

**Solução:** Verificar se `dashboards/templates/dashboards/dashboard_samc.html` existe

### 3. URL Not Found

**Causa:** Rotas não incluídas

**Solução:** Verificar `projeto_saacb/urls.py` tem `include('dashboards.urls')`

### 4. Permission Denied

**Causa:** Usuário não autenticado

**Solução:** Fazer login

---

## 📚 REFERÊNCIAS

### Documentação Django

- [Apps Django](https://docs.djangoproject.com/en/4.2/ref/applications/)
- [Views Django](https://docs.djangoproject.com/en/4.2/topics/http/views/)
- [URLs Django](https://docs.djangoproject.com/en/4.2/topics/http/urls/)

### Dashboard Original

- **Localização:** `Dashboard SAMC/index.html`
- **Tecnologias:** React 18, Tailwind CSS, Recharts 2.12.7, Paparse 5.4.1
- **Nota:** Original era standalone (sem backend Django)

---

## ✅ CHECKLIST FINAL

- [x] App `dashboards` criado
- [x] Views Django criadas
- [x] Templates React criados
- [x] URLs configuradas
- [x] INSTALLED_APPS atualizado
- [x] Permissões implementadas (admin vs usuário)
- [x] Exportação CSV funcionando
- [x] Visualização de dados do banco
- [x] KPIs calculados
- [x] Gráficos (Pie, Bar)
- [x] Filtros (busca, status)
- [x] Ordenação de tabela
- [x] Modal de detalhes
- [x] Link para admin

---

**Versão:** 1.0  
**Data:** 2026-03-21  
**Status:** ✅ INTEGRAÇÃO COMPLETA  
**Próximo:** Deploy em servidor
