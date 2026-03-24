# ✅ Atualização Completa - Cloudflare Tunnel Configurado

## 📦 O Que Foi Feito

### 1. ✅ docker-compose-prod.yml Atualizado

**Alteração:**
```yaml
# Antes
CALCULADORA_API_URL=http://planilha-calculos-prod:8000

# Depois
CALCULADORA_API_URL=https://calculadora.saacb.lakeserver.online
```

**Nova URL:** `https://calculadora.saacb.lakeserver.online`

Esta URL vai redirecionar para o Cloudflare Tunnel da porta 8002.

### 2. ✅ Commit e Push Realizados

| Commit | Mensagem | Repositórios |
|--------|----------|--------------|
| `9e27b63` | fix: atualizar CALCULADORA_API_URL para Cloudflare Tunnel | origin + prod |

---

## 🌐 Como Configurar o Cloudflare Tunnel

### Passo 1: Criar Subdomínio no Cloudflare

1. Acesse: https://dash.cloudflare.com/
2. Selecione seu domínio: `saacb.lakeserver.online`
3. Clique em: **DNS** → **Records**
4. Clique em: **Add record**
5. Preencha:
   - **Type:** `CNAME`
   - **Name:** `calculadora`
   - **Target:** Seu Cloudflare Tunnel hostname (ex: `seu-tunnel.trycloudflare.com`)
   - **Proxy status:** ✅ Proxied
   - **TTL:** Auto

### Passo 2: Criar o Cloudflare Tunnel

1. Vá em: https://dash.cloudflare.com/zero-trust
2. Clique em: **Access** → **Tunnels**
3. Clique em: **Create a tunnel**
4. Preencha:
   - **Tunnel name:** `saacb-calculadora` (ou qualquer nome)
   - **Tunnel type:** `Cloudflare` (padrão) → **Next**
5. Selecione: **Free** → **Next**
6. Configure:
   - **Subdomain:** `calculadora`
   - **Domain:** `saacb.lakeserver.online`
   - Clique em: **Save tunnel**

### Passo 3: Copiar o Comando do Tunnel

1. No Cloudflare, selecione o tunnel criado
2. Clique em: **Install and Run cloudflared**
3. Selecione: **Debian/Ubuntu** (CasaOS é Debian)
4. Clique em: **Copy command**
5. O comando será algo como:
   ```bash
   curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 && chmod +x cloudflared && sudo ./cloudflared tunnel --url https://SEU_TUNNEL_ID.trycloudflare.com --token SEU_TOKEN_AQUI
   ```

### Passo 4: Executar no CasaOS

```bash
# Baixar cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared

# Executar o comando (substitua pelo seu)
sudo ./cloudflared tunnel --url https://SEU_TUNNEL_ID.trycloudflare.com --token SEU_TOKEN_AQUI
```

---

## 🚀 Como Atualizar o Servidor

### Opção 1: Pull e Reiniciar (Recomendado)

```bash
cd /DATA/AppData/saacb-django-prod

# Atualizar docker-compose.yml
git pull origin main

# Reiniciar containers
docker compose down
docker compose up -d
```

### Opção 2: Copiar Arquivo Manualmente

```bash
cp /DATA/AppData/saacb-django-prod/docker-compose.yml.backup-$(date +%Y%m%d-%H%M%S) /DATA/AppData/saacb-django-prod/docker-compose.yml
nano /DATA/AppData/saacb-django-prod/docker-compose.yml
```

---

## 📊 Arquitetura Final

```
Internet (443/80)
    ↓
Cloudflare (saacb.lakeserver.online)
    ↓ (HTTPS)
    ↓
calculadora.saacb.lakeserver.online (CNAME)
    ↓ (DNS)
    ↓
Cloudflare Tunnel (calculadora.saacb)
    ↓
CasaOS:8002 → planilha-calculos-prod:8000 (Docker)
```

---

## ✅ Verificação

### Teste 1: Via Browser

```bash
# Teste 1: Via Cloudflare (externo)
curl https://calculadora.saacb.lakeserver.online/api/status
# Deve retornar JSON da API

# Teste 2: Via Docker (interno)
curl http://localhost:8002/api/status
# Deve retornar o mesmo JSON
```

### Teste 2: Via SAACB Django

1. Acesse: https://saacb.lakeserver.online
2. Abra a página de cálculos
3. Tente realizar um cálculo
4. Deve funcionar normalmente!

---

## 📋 Checklist de Configuração

- [ ] Subdomínio DNS criado (`calculadora.saacb.lakeserver.online`)
- [ ] Cloudflare Tunnel criado
- [ ] cloudflared instalado no CasaOS
- [ ] cloudflared executado e rodando
- [ ] docker-compose.yml atualizado com nova URL
- [ ] Containers reiniciados
- [ ] Teste externo funcionando (HTTPS)
- [ ] Teste interno funcionando (Docker)
- [ ] SAACB fazendo cálculos normalmente

---

## 📦 Commits Relacionados

| Commit | Mensagem |
|--------|----------|
| `9e27b63` | fix: atualizar CALCULADORA_API_URL para Cloudflare Tunnel |

---

**Última atualização:** 2026-03-23
**Nova URL da calculadora:** `https://calculadora.saacb.lakeserver.online`
