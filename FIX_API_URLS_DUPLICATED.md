# 🔧 Correção das URLs Duplicadas da API de Cálculos

## ❌ Problema

Erro nos logs do Django:
```
Not Found: /api//api/status
Not Found: /api//api/indices-padrao
Not Found: /api//api/upload-pdf
```

## 🔍 Causa

No template `calcular_creditos.html`, a URL base estava incorreta:

```javascript
// CÓDIGO INCORRETO ❌
const isProduction = window.location.hostname === 'saacb.lakeserver.online';
const API_BASE = isProduction ? '/api/' : 'http://192.168.1.51:8002';

// Depois nos fetches:
fetch(`${API_BASE}/api/status`)
// Em produção: '/api/' + '/api/status' = '/api//api/status' ❌
```

**Em produção**, `API_BASE = '/api/'` (com barra no final), resultando em duplicação.

## ✅ Solução

### 1. Correção em desenvolvimento

```javascript
// CÓDIGO CORRETO ✅
const isProduction = window.location.hostname === 'saacb.lakeserver.online';
const API_BASE = isProduction ? '/api' : 'http://192.168.1.51:8002';

// Depois nos fetches:
fetch(`${API_BASE}/status`)
fetch(`${API_BASE}/indices-padrao`)
fetch(`${API_BASE}/upload-pdf`)
fetch(`${API_BASE}/calcular`)
```

**Em produção:**
- `API_BASE = '/api'` (sem barra no final)
- URLs: `/api/status`, `/api/indices-padrao`, `/api/upload-pdf`, `/api/calcular`

**Em dev:**
- `API_BASE = 'http://192.168.1.51:8002'`
- URLs: `http://192.168.1.51:8002/status` (com problema)

### 2. Solução Compatível

Para manter compatibilidade com dev e produção, o ideal é usar proxy reverso:

**Em produção (saacb.lakeserver.online):**
```nginx
# Proxy reverso nginx
location /api/ {
    proxy_pass http://planilha-calculos-prod:8000/api/;
    proxy_set_header Host $host;
}
```

**Em dev (192.168.1.51):**
- Acessar a API diretamente em `http://192.168.1.51:8002`

## 🚀 Como Aplicar a Correção no Servidor

### Opção Rápida: Script

```bash
bash /tmp/fix-api-urls.sh
```

### Opção Manual

```bash
# Copiar arquivo corrigido
cp /tmp/calcular_creditos.html /DATA/AppData/saacb-django-prod/tarefas/templates/tarefas/integracao/

# Reiniciar container
cd /DATA/AppData/saacb-django-prod
docker compose restart saacb-prod
```

### Opção Git Pull

```bash
cd /DATA/AppData/saacb-django-prod
git pull origin main
docker compose restart saacb-prod
```

## 📊 Tabela de URLs

| Ambiente | API_BASE | URLs Resultantes |
|----------|-----------|-----------------|
| **Produção** | `/api` | `/api/status`, `/api/indices-padrao`, `/api/upload-pdf`, `/api/calcular` |
| **Dev** | `http://192.168.1.51:8002` | `http://192.168.1.51:8002/status` (precisa de proxy) |

## 📝 Nota Importante

**Em produção**, para que as URLs funcionem corretamente, é necessário configurar um **proxy reverso** que redirecione `/api/*` para o container da planilha-calculos.

Se o proxy não estiver configurado, as requisições para `/api/*` serão tratadas pelo próprio Django, não pela API de cálculos.

## 📦 Commits Realizados

| Commit | Mensagem |
|--------|----------|
| `0f68ed9` | fix: corrigir URLs duplicadas da API de cálculos em produção |

---

**Última atualização:** 2026-03-23
