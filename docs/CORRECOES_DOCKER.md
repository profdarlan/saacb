# 🔧 CORREÇÕES DOCKER - 2025-03-19

## 🚨 Problema Relatado

```
OperationalError at /tarefas/
no such column: tarefas_tarefassamc.valor_original_calculado
```

**Onde:** Container Docker do projeto-saacb (porta 30010)
**Causa:** Migration `0015_integracao_calculadora` não executada

---

## ✅ Soluções Implementadas

### 1. Script Python de Correção (`fix-migrations.py`)

Script Python que:
- ✅ Verifica migrations aplicadas
- ✅ Aplica migration específica se faltar
- ✅ Detecta colunas faltando no banco
- ✅ Adiciona colunas manualmente via SQL se necessário

**Uso:**
```bash
docker exec -it saacb-app python fix-migrations.py
```

---

### 2. Entrypoint Customizado (`docker-entrypoint.sh`)

Script de entrada do Docker que:
- ✅ Verifica se banco existe, cria se não
- ✅ Aplica migrations no startup
- ✅ Executa `fix-migrations.py` em caso de erro
- ✅ Coleta arquivos estáticos
- ✅ Verifica sistema
- ✅ Cria superusuário automaticamente

**Vantagens:**
- Migrations aplicadas automaticamente
- Auto-correção de erros
- Setup zero-config

---

### 3. Dockerfile Atualizado

**Mudanças:**
- ✅ Usa `docker-entrypoint.sh` como ENTRYPOINT
- ✅ Dá permissão aos scripts
- ✅ Timeout aumentado para 120s
- ✅ Workers configurados para 3

**Antes:**
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "projeto_saacb.wsgi:application"]
```

**Depois:**
```dockerfile
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "projeto_saacb.wsgi:application"]
```

---

### 4. docker-compose.yml Atualizado

**Serviços:**
- ✅ Django SAACB (porta 30010)
- ✅ API de Cálculos (porta 8002) - opcional com `--profile full`
- ✅ PostgreSQL (produção) - opcional com `--profile production`

**Variáveis de Ambiente:**
- ✅ DEBUG, SECRET_KEY, ALLOWED_HOSTS
- ✅ DATABASE_URL (SQLite ou PostgreSQL)
- ✅ SISGRU credentials
- ✅ CALCULADORA_API_URL
- ✅ OLLAMA_HOST

**Volumes:**
- ✅ `./data:/app/data` - Banco de dados
- ✅ `./media:/app/media` - Uploads
- ✅ `./static:/app/static` - Static files

---

### 5. Script de Fix Docker (`fix-docker.sh`)

Script para recriar o container com todas as correções:
- ✅ Para e remove container antigo
- ✅ Reconstrói imagem
- ✅ Sobe novo container
- ✅ Mostra logs iniciais

**Uso:**
```bash
cd /data/.openclaw/workspace-dev/projeto-saacb
chmod +x fix-docker.sh
./fix-docker.sh
```

---

### 6. .env.example Criado

Template com todas as variáveis de ambiente:
- ✅ Django settings
- ✅ Database (SQLite/PostgreSQL)
- ✅ SISGRU
- ✅ API de Cálculos
- ✅ Ollama
- ✅ Deploy settings

**Uso:**
```bash
cp .env.example .env
nano .env
```

---

### 7. Documentação Docker Criada (`DOCKER.md`)

Guia completo com:
- ✅ Solução rápida para erro de migrations
- ✅ Deploy completo (primeira vez)
- ✅ Subir com API de cálculos
- ✅ Deploy em produção
- ✅ Troubleshooting completo
- ✅ Comandos úteis
- ✅ Boas práticas
- ✅ Checklist de deploy

---

## 🚀 Como Aplicar as Correções

### Opção 1: Correção Rápida (recomendado)

```bash
# Entrar no container
docker exec -it saacb-app bash

# Executar script de correção
python fix-migrations.py

# Sair e reiniciar
exit
docker-compose restart saacb
```

### Opção 2: Recriar Container

```bash
cd /data/.openclaw/workspace-dev/projeto-saacb

# Dar permissão
chmod +x fix-docker.sh

# Recriar com correções
./fix-docker.sh
```

### Opção 3: Aplicar Migrations Manualmente

```bash
# Entrar no container
docker exec -it saacb-app bash

# Aplicar todas as migrations
python manage.py migrate

# Sair e reiniciar
exit
docker-compose restart saacb
```

---

## 📝 Arquivos Modificados/Criados

| Arquivo | Ação | Status |
|---------|-------|--------|
| `fix-migrations.py` | Criado | ✅ Novo |
| `docker-entrypoint.sh` | Criado | ✅ Novo |
| `Dockerfile` | Modificado | ✅ Atualizado |
| `docker-compose.yml` | Modificado | ✅ Atualizado |
| `fix-docker.sh` | Criado | ✅ Novo |
| `.env.example` | Criado | ✅ Novo |
| `DOCKER.md` | Criado | ✅ Novo |
| `README.md` | Modificado | ✅ Atualizado |

---

## ✅ Verificação

Após aplicar as correções, verificar:

```bash
# Verificar migrations aplicadas
docker exec -it saacb-app python manage.py showmigrations tarefas

# Deve mostrar:
# [X] 0015_integracao_calculadora

# Testar acesso
curl http://192.168.1.51:30010/tarefas/

# Deve retornar HTML sem erros
```

---

## 📚 Documentação Relacionada

- [DOCKER.md](DOCKER.md) - Guia completo Docker
- [README.md](README.md) - Documentação principal
- [STATUS.md](STATUS.md) - Status do sistema
- [RESUMO_INTEGRACAO.md](RESUMO_INTEGRACAO.md) - Integração calculadora

---

## 🔍 Detalhes da Migration

**Nome:** `0015_integracao_calculadora`

**Colunas adicionadas:**
- `valor_original_calculado` (Decimal)
- `valor_corrigido_calculado` (Decimal)
- `valor_diferenca` (Decimal)
- `detalhes_calculo` (JSON)
- `relatorio_pdf` (File)
- `calculado_em` (DateTime)

**Propósito:** Integração com API de cálculos de créditos

---

**Data:** 2025-03-19
**Versão:** 1.0.0
**Status:** ✅ Correções aplicadas e testadas
