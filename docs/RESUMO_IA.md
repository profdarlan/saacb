# 📋 RESUMO SAACB - Guia Rápido para IA

**Versão:** 1.0  
**Data:** 2026-03-21

---

## 🎯 O QUE É SAACB?

Sistema Django para gestão de tarefas de análise do INSS, com:
- CRUD de tarefas de análise administrativa
- Geração de documentos (ofícios, despachos)
- Integração SISGRU (GRUs Governo)
- Cálculo de créditos via API externa

---

## 🏗️ ARQUITETURA

```
projeto-saacb/
├── projeto_saacb/          # Config Django (settings, urls, wsgi)
├── tarefas/                # App principal
│   ├── models.py           # Model: tarefassamc, GRU, etc.
│   ├── views.py            # Views CRUD, listagem, etc.
│   ├── views_integracao.py # Views cálculos (API)
│   ├── admin.py            # Django Admin config
│   ├── services.py         # Geração de documentos
│   ├── gru/gru_service.py  # Integração SISGRU
│   └── integracao/         # Cliente API cálculos
├── templates/              # Templates globais
├── static/                 # CSS, JS
└── media/                  # Uploads
```

---

## 📊 MODELO PRINCIPAL: tarefassamc

**Campos principais:**
- `nome_interessado`, `CPF`
- `tarefa_n`, `sei_n`, `procj`
- `nb1`, `nb2` (benefícios)
- `servico` (choices: ANALISE, CONCLUIDO, PA, PERICIA, etc.)
- `status` (choices: PENDENTE, CONCLUIDA_INTERMEDIARIA, CONCLUIDA_FINALIZADA)
- `Conclusao` (choices: REGULAR, IRREGULAR Boa fé, IRREGULAR Má fé)
- `valor`, `Competencia`, `Periodo_irregular`
- `assigned_user` (FK User)
- `concluida_em` (preenchido automaticamente quando status concluído)

**Campos integração (cálculos):**
- `valor_original_calculado` (DecimalField)
- `valor_corrigido_calculado` (DecimalField)
- `valor_diferenca` (DecimalField)
- `detalhes_calculo` (JSONField)
- `relatorio_pdf` (FileField)
- `calculado_em` (DateTimeField)

---

## 🔗 ROTAS PRINCIPAIS

| Rota | View | Método | Descrição |
|------|------|--------|-----------|
| `/tarefas/` | TarefaListView | GET | Lista tarefas |
| `/tarefas/lista/` | TarefaListOrdenadaView | GET | Lista moderna (ordenável) |
| `/tarefas/<pk>/` | TarefaDetailView | GET | Detalhes tarefa |
| `/tarefas/create/` | TarefaCreateView | GET/POST | Criar tarefa |
| `/tarefas/<pk>/update/` | TarefaUpdateView | GET/POST | Editar tarefa |
| `/tarefas/tarefa/<id>/calcular/` | calcular_creditos_tarefa | GET/POST | Calcular créditos |
| `/tarefas/api/calcular/` | calcular_ajax | POST | Calcular AJAX |
| `/tarefas/tarefa/<id>/pdf/` | baixar_relatorio_pdf | POST | Baixar PDF |
| `/tarefas/tarefa/<id>/excel/` | baixar_relatorio_excel | POST | Baixar Excel |
| `/tarefas/api/status/` | status_api | GET | Status API cálculos |
| `/tarefas/tarefa/<pk>/gerar/<tipo>/` | GerarDocumentoView | GET | Gerar documento |
| `/gru/` | GRUListView | GET | Lista GRUs |

**Namespace:** `tarefas` (usar `{% url 'tarefas:tarefa_detail' %}`)

---

## 🔌 INTEGRAÇÕES

### 1. API de Cálculos (Planilha SAACB)

**URL:** `http://192.168.1.51:8002`

**Endpoints:**
- `POST /api/calcular` - Calcular correção
- `POST /api/gerar-excel` - Gerar Excel
- `POST /api/gerar-relatorio-pdf` - Gerar PDF
- `GET /api/indices-padrao` - Obter índices
- `GET /` - Health check

**Cliente:** `tarefas/integracao/calculadora_client.py`

**Data Classes:**
```python
BeneficiarioData(numero_beneficio, nome_titular, ...)
CreditoData(competencia, valor_original, ...)
IndiceData(competencia, indice)
CalculoResultado(total_original, total_corrigido, diferenca, ...)
```

### 2. SISGRU (Governo)

**URLs:**
- Homologação: `https://webservice-sisgru-hml.tesouro.gov.br/sisgru/services/v1`
- Produção: `https://webservice-sisgru.tesouro.gov.br/sisgru/services/v1`

**Horário:** Seg-Sex, 08:00-22:00 (Brasília)

**Cliente:** `tarefas/gru/gru_service.py`

**Métodos:**
- `consultar_gru(numero_gru)` - Consulta GRU
- `validar_numero_gru(numero_gru)` - Valida formato (32 dígitos)

---

## 🐛 ERROS CONHECIDOS

| Erro | Causa | Solução |
|------|-------|----------|
| `NoReverseMatch: 'tarefa_detail' with keyword arguments '{'tarefa_id': 88}'` | Parâmetro errado no redirect() | Usar `pk=` em vez de `tarefa_id=` |
| `NoReverseMatch: Reverse for 'detail' not found` | Nome da URL incorreto em `views_integracao.py` | Usar `'tarefas:tarefa_detail'` em vez de `'tarefas:detail'` |
| `TemplateDoesNotExist: tarefas/calcular_creditos.html` | Path errado em views_integracao.py | Mudar para `'tarefas/integracao/calcular_creditos.html'` |
| `NoReverseMatch: Reverse for 'tarefa_list'` | URL sem namespace | Usar `{% url 'tarefas:tarefa_list' %}` |
| `no such column: tarefas_tarefassamc.valor_original_calculado` | Migration não aplicada | `python manage.py migrate` |
| API cálculos offline | Container não rodando | Verificar `docker ps`, subir container |
| SISGRU indisponível | Fora do horário ou credenciais | Verificar horário e `.env` |
| Database locked | SQLite concorrência | Usar PostgreSQL em produção |
| Static files não encontradas | `collectstatic` não executado | `python manage.py collectstatic` |
| AttributeError 'NoneType' | assigned_user None | Acesso defensivo: `au.username if au else ''` |
| PDF desabilitado | xhtml2pdf conflito | Usar API cálculos para PDF |

---

## 🛠️ COMANDOS ÚTEIS

```bash
# Django
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell
python manage.py createsuperuser
python manage.py showmigrations

# Docker
docker-compose up -d
docker-compose logs -f saacb
docker exec -it saacb-django-teste python manage.py shell
docker cp arquivo.txt saacb-django-teste:/app/

# Diagnóstico
python diagnostico_completo.py
python testar_integracao.py
```

---

## 📁 ARQUIVOS IMPORTANTES

| Arquivo | Descrição |
|---------|-----------|
| `MAPEAMENTO_SISTEMA_IA.md` | Documento completo (este) |
| `RESUMO_IA.md` | Este resumo |
| `README.md` | Documentação principal |
| `STATUS.md` | Status do sistema |
| `tarefas/models.py` | Modelos de dados |
| `tarefas/views.py` | Views principais |
| `tarefas/views_integracao.py` | Views integração |
| `tarefas/admin.py` | Django Admin |
| `tarefas/services.py` | Geração documentos |
| `tarefas/integracao/calculadora_client.py` | Cliente API cálculos |
| `tarefas/gru/gru_service.py` | Cliente SISGRU |
| `projeto_saacb/settings.py` | Configurações |
| `requirements.txt` | Dependências |
| `.env` | Variáveis de ambiente |

---

## 🔍 CHECKLIST DEBUG

1. [ ] Reproduzir erro (anotar passos)
2. [ ] Verificar logs Django/Gunicorn
3. [ ] Verificar logs browser console
4. [ ] `python manage.py showmigrations` (migrations aplicadas?)
5. [ ] Verificar APIs (ping)
6. [ ] Verificar `.env`
7. [ ] Verificar permissões arquivos/templates
8. [ ] `python manage.py collectstatic` (static files?)
9. [ ] `python manage.py check --deploy`
10. [ ] Consultar erros conhecidos
11. [ ] `python diagnostico_completo.py`

---

## 📦 VARIÁVEIS DE AMBIENTE

```bash
# Django
DEBUG=True
SECRET_KEY=django-insecure-chave
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.51

# SISGRU
SISGRU_USUARIO=usuario
SISGRU_SENHA=senha
SISGRU_PRODUCAO=False

# API Cálculos
CALCULADORA_API_URL=http://192.168.1.51:8002
CALCULADORA_API_TOKEN=

# Database
DATABASE_URL=sqlite:////app/data/db.sqlite3
```

---

## 🎯 FLUXO DE CÁLCULO DE CRÉDITOS

```
1. POST /tarefas/tarefa/<id>/calcular/
2. views_integracao.calcular_creditos_tarefa
3. tarefa_para_calculo(tarefa) → BeneficiarioData, CreditoData[]
4. client.obter_indices_padrao() → IndiceData[]
5. client.calcular(beneficiario, creditos, indices) → CalculoResultado
6. Atualizar tarefa:
   - valor_original_calculado
   - valor_corrigido_calculado
   - valor_diferenca
   - detalhes_calculo (JSON)
   - calculado_em
7. tarefa.save()
8. Redirect ou baixar PDF/Excel
```

---

## 💡 DICAS RÁPIDAS

- **Templates:** Sempre usar namespace `tarefas:` nas URLs
- **Migrations:** Verificar se `0003_integracao_calculadora.py` está aplicada
- **Static files:** WhiteNoise deve ser o 2º middleware
- **Debug:** Usar `diagnostico_completo.py` para verificação geral
- **SISGRU:** Só funciona 08:00-22:00 Seg-Sex (Brasília)
- **API Cálculos:** Verificar se está rodando na porta 8002
- **Assigned User:** Sempre fazer acesso defensivo (`if au else ''`)
- **Valor monetário:** Normalizar (remove pontos, troca vírgula por ponto)

---

**Documento completo:** `MAPEAMENTO_SISTEMA_IA.md`  
**Resumo rápido:** `RESUMO_IA.md` (este arquivo)
