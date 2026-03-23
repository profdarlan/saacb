# 🔧 Correção da URL da API de Cálculos

## ❌ Problema

O sistema SAACB não consegue conectar à API de cálculos:
```
Status API: API de cálculos indisponível
```

## 🔍 Causa

A `CALCULADORA_API_URL` no `docker-compose-prod.yml` estava configurada para:
```yaml
CALCULADORA_API_URL=http://saacb.lakeserver.online:8000  # ❌ Errado
```

Esta URL **não existe**. O container da planilha-calculos está rodando na rede Docker interna.

## ✅ Solução

A URL correta para comunicação interna entre containers é:
```yaml
CALCULADORA_API_URL=http://planilha-calculos-prod:8000  # ✅ Correto
```

## 🚀 Como Aplicar a Correção

### Opção 1: Usar o script (recomendado)
```bash
cd /DATA/AppData/saacd-django-prod
bash /tmp/fix-calculadora-url.sh
```

### Opção 2: Manualmente

1. **Copiar o arquivo atualizado do repositório:**
   ```bash
   cp /tmp/docker-compose-prod.yml /DATA/AppData/saacb-django-prod/docker-compose.yml
   ```

2. **Ou editar manualmente o docker-compose.yml:**
   ```bash
   cd /DATA/AppData/saacb-django-prod
   nano docker-compose.yml
   ```
   Alterar:
   ```yaml
   - CALCULADORA_API_URL=http://planilha-calculos-prod:8000
   ```

3. **Reiniciar o container Django:**
   ```bash
   docker compose restart saacb-prod
   ```

### Opção 3: Reiniciar tudo
```bash
cd /DATA/AppData/saacb-django-prod
docker compose down
docker compose up -d --build
```

## 🧪 Verificação

Testar se o container Django consegue acessar a API:
```bash
docker exec saacb-django-prod python -c "import requests; r = requests.get('http://planilha-calculos-prod:8000/'); print('Status:', r.status_code)"
```

Resultado esperado:
```
Status: 200
```

## 📊 Informações dos Containers

| Container | Nome | Rede | Porta Host |
|-----------|------|-------|-------------|
| SAACB Produção | saacb-django-prod | saacb-prod-network | 8000 |
| Planilha Calculos | planilha-calculos-prod | saacb-prod-network | 8002 |

Ambos os containers estão na mesma rede Docker: `saacb-prod-network`

## 📝 Commits Realizados

| Commit | Mensagem |
|--------|----------|
| `5e161f1` | fix: corrigir URL da API de cálculos em produção |

---

**Última atualização:** 2026-03-23
