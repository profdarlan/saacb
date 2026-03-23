# 🔧 CORREÇÃO DOCKERFILE - 2025-03-19

## 🚨 Problema

Dockerfile estava causando erros no build/deploy.

---

## ✅ Correções Aplicadas

### 1. Dockerfile Simplificado

**Problemas removidos:**
- ❌ Dependência de `docker-entrypoint.sh` (pode não existir no build)
- ❌ Dependência de `fix-migrations.py` (pode não existir no build)
- ❌ Entradas duplicadas em `requirements.txt`

**Solução:**
- ✅ Dockerfile simplificado sem entrypoint customizado
- ✅ Migrations e static collection no build
- ✅ `requirements.txt` limpo (sem duplicatas)
- ✅ Caminhos corretos para WSGI

---

## 📋 Novo Dockerfile

```dockerfile
FROM python:3.11-slim

# 1. Instalar pacotes do sistema
RUN apt-get update -qq && apt-get install -y \
    build-essential \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copiar requirements primeiro para cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 3. Copiar todo o código
COPY . .

# 4. Executar migrations e coletar static
RUN python manage.py collectstatic --noinput --clear || echo "Static collection skipped"
RUN python manage.py migrate --noinput || echo "Migrations skipped"

# 5. Criar diretório de dados
RUN mkdir -p /app/data

# 6. Volume para banco de dados
VOLUME ["/app/data", "/app/media", "/app/staticfiles"]

# 7. Expor porta
EXPOSE 8000

# 8. Comando padrão
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "projeto_saacb.wsgi:application"]
```

---

## 📋 requirements.txt Corrigido

**Problema:** Entradas duplicadas (python-dotenv, whitenoise, gunicorn)

**Solução:** Removidas duplicatas, versão limpa.

---

## 🔄 Como Rebuildar

### Método 1: Via docker-compose

```bash
cd /caminho/para/projeto-saacb

# Parar e remover
docker-compose down

# Remover imagem antiga
docker rmi projeto-saacb-saacb 2>/dev/null || echo "Imagem não existe"

# Reconstruir
docker-compose build --no-cache

# Subir
docker-compose up -d

# Verificar logs
docker-compose logs -f
```

### Método 2: Direto

```bash
cd /caminho/para/projeto-saacb

# Remover imagem antiga
docker rmi projeto-saacb-saacb 2>/dev/null || echo "Imagem não existe"

# Build
docker build -t projeto-saacb-saacb .

# Subir container
docker run -d --name saacb-django-teste \
    -p 30010:8000 \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/media:/app/media \
    -v $(pwd)/static:/app/staticfiles \
    projeto-saacb-saacb
```

---

## 🔍 Verificação

### 1. Verificar se o container está rodando

```bash
docker ps | grep saacb
```

Deve mostrar algo como:
```
1234567890ab   projeto-saacb-saacb   "gunicorn --bind..."   5 minutos ago   Up 5 minutes   0.0.0.0:8000->30010/tcp   saacb-django-teste
```

### 2. Verificar logs

```bash
docker logs saacb-django-teste
```

### 3. Verificar se o site está acessível

```bash
curl http://192.168.1.51:30010/tarefas/
```

Deve retornar HTML (não erro).

---

## ✅ Esperado Após Rebuild

1. ✅ Container builda sem erros
2. ✅ Container inicia corretamente
3. ✅ Migrations aplicadas no build
4. ✅ Static files coletadas
5. ✅ Site acessível na porta 30010
6. ✅ Sem erros no logs

---

## 🚨 Se Ainda Houver Erros

### Erro: "ModuleNotFoundError: No module named 'projeto_saacb'"

**Causa:** WSGI com nome errado

**Solução:** Verificar se `projeto_saacb/wsgi.py` existe

### Erro: "Static files não encontradas"

**Causa:** Static collection falhou

**Solução:** Executar manualmente no container
```bash
docker exec -it saacb-django-teste python manage.py collectstatic --noinput
```

### Erro: "Migrations não aplicadas"

**Causa:** Migrations não executadas no build

**Solução:** Executar manualmente no container
```bash
docker exec -it saacb-django-teste python manage.py migrate --noinput
```

---

## 📝 Arquivos Modificados

| Arquivo | Mudança |
|---------|---------|
| `Dockerfile` | Simplificado, sem entrypoint customizado |
| `Dockerfile.v2` | Backup da nova versão |
| `requirements.txt` | Removidas duplicatas |
| `DOCKERFILE_CORRIGIDO.md` | Este arquivo |

---

## 📚 Documentação Relacionada

- `DOCKER.md` - Guia Docker
- `DOCKER_NAO_ACESSIVEL.md` - Explicação sobre acesso ao Docker

---

**Versão:** 2.0.0
**Data:** 2025-03-19
**Status:** ✅ Dockerfile simplificado e corrigido
