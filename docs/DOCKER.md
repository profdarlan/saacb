# 🐳 Guia de Deploy Docker - SAACB

## 🚨 Solução para Erro de Migrations

### Problema

```
OperationalError at /tarefas/
no such column: tarefas_tarefassamc.valor_original_calculado
```

### Causa

A migration `0015_integracao_calculadora` não foi executada no banco de dados do container Docker.

---

## ✅ Solução Rápida

### Opção 1: Executar script de correção dentro do container

```bash
# Entrar no container
docker exec -it saacb-django-teste bash

# Executar script de correção
python fix-migrations.py

# Sair do container
exit

# Reiniciar container
docker-compose restart saacb
```

### Opção 2: Recriar o container com as correções

```bash
# Baixar scripts atualizados
cd /data/.openclaw/workspace-dev/projeto-saacb

# Dar permissão
chmod +x fix-docker.sh

# Executar correção
./fix-docker.sh
```

### Opção 3: Executar migrate manualmente

```bash
# Entrar no container
docker exec -it saacb-django-teste bash

# Aplicar migrations
python manage.py migrate

# Sair
exit

# Reiniciar
docker-compose restart saacb
```

---

## 📋 Deploy Completo (Primeira Vez)

### Passo 1: Configurar Variáveis de Ambiente

```bash
cd /data/.openclaw/workspace-dev/projeto-saacb

# Criar arquivo .env a partir do exemplo
cp .env.example .env

# Editar conforme necessário
nano .env
```

### Passo 2: Construir e Subir

```bash
# Construir imagem
docker-compose build

# Subir container
docker-compose up -d
```

### Passo 3: Verificar Status

```bash
# Ver logs
docker-compose logs -f saacb

# Ver se está rodando
docker-compose ps

# Testar acesso
curl http://localhost:30010/
```

### Passo 4: Criar Superusuário

```bash
# Entrar no container
docker exec -it saacb-app bash

# Criar superusuário
python manage.py createsuperuser

# Sair
exit
```

### Passo 5: Acessar Sistema

- **Sistema:** http://192.168.1.51:30010
- **Admin:** http://192.168.1.51:30010/admin/
- **Usuário:** admin
- **Senha:** admin123 (criado pelo entrypoint)

---

## 🔧 Arquivos Criados para Correção

### 1. `fix-migrations.py`
Script Python para aplicar migrations de integração manualmente.

**Uso:**
```bash
docker exec -it saacb-app python fix-migrations.py
```

### 2. `docker-entrypoint.sh`
Script de entrada do Docker que garante migrations sejam aplicadas.

**Funcionalidades:**
- ✅ Aplica migrations no startup
- ✅ Detecta e corrige erros
- ✅ Coleta arquivos estáticos
- ✅ Cria superusuário automaticamente
- ✅ Verifica sistema antes de iniciar

### 3. `Dockerfile` (atualizado)
Novo Dockerfile com entrypoint customizado.

**Mudanças:**
- ✅ Usa `docker-entrypoint.sh` como entrypoint
- ✅ Executa migrations automaticamente
- ✅ Timeout aumentado para 120s
- ✅ Permissões configuradas

### 4. `docker-compose.yml` (atualizado)
Arquivo compose completo com todos os serviços.

**Serviços:**
- ✅ Django SAACB
- ✅ API de Cálculos (opcional)
- ✅ PostgreSQL (opcional, produção)

### 5. `fix-docker.sh`
Script para recriar container com correções.

**Uso:**
```bash
./fix-docker.sh
```

---

## 🚀 Subir com API de Cálculos

Para subir o sistema completo com a API de cálculos:

```bash
# Subir todos os serviços
docker-compose --profile full up -d

# Ver logs
docker-compose logs -f
```

---

## 🏭 Deploy em Produção

### 1. Usar PostgreSQL

```bash
# Subir com PostgreSQL
docker-compose --profile production up -d
```

### 2. Configurar Segurança

No `.env`:
```bash
DEBUG=False
SECRET_KEY=sua_chave_secreta_real
ALLOWED_HOSTS=seu_dominio.com
SISGRU_PRODUCAO=True
```

### 3. Configurar HTTPS

Use nginx ou traefik como reverse proxy.

---

## 🔍 Troubleshooting

### Erro: "no such column"

**Solução:**
```bash
docker exec -it saacb-app python fix-migrations.py
```

### Erro: "Database locked"

**Solução:**
```bash
docker-compose restart saacb
```

### Erro: "Permission denied"

**Solução:**
```bash
docker-compose down
chmod +x docker-entrypoint.sh
chmod +x fix-migrations.py
docker-compose up -d
```

### Verificar logs

```bash
# Logs do container
docker logs saacb-app --tail 100

# Logs do compose
docker-compose logs -f

# Logs específicos do Django
docker exec -it saacb-app tail -f /tmp/*.log
```

### Entrar no container

```bash
# Shell interativo
docker exec -it saacb-app bash

# Django shell
docker exec -it saacb-app python manage.py shell

# Ver migrations
docker exec -it saacb-app python manage.py showmigrations
```

---

## 📝 Comandos Úteis

### Docker Compose

```bash
# Subir containers
docker-compose up -d

# Parar containers
docker-compose down

# Reiniciar
docker-compose restart

# Ver logs
docker-compose logs -f

# Reconstruir
docker-compose build
docker-compose up -d
```

### Docker (direto)

```bash
# Ver containers rodando
docker ps

# Ver todos os containers
docker ps -a

# Ver logs de container
docker logs saacb-app

# Entrar no container
docker exec -it saacb-app bash

# Copiar arquivo para container
docker cp local.txt saacb-app:/app/

# Copiar arquivo do container
docker cp saacb-app:/app/db.sqlite3 local_backup.sqlite
```

---

## 🎯 Boas Práticas

### 1. Sempre usar volumes

```yaml
volumes:
  - ./data:/app/data
  - ./media:/app/media
  - ./static:/app/static
```

### 2. Usar .env para configurações

```bash
cp .env.example .env
nano .env
```

### 3. Versionar migrations

```bash
# Sempre commitar migrations
git add tarefas/migrations/
git commit -m "Add migration XYZ"
```

### 4. Testar antes de deploy

```bash
# Testar localmente
python manage.py migrate
python manage.py check

# Só depois deploy em Docker
docker-compose up -d
```

---

## 📚 Documentação Adicional

- [README.md](README.md) - Documentação principal
- [STATUS.md](STATUS.md) - Status do sistema
- [GUIA_SISGRU.md](tarefas/gru/GUIA_SISGRU.md) - Integração SISGRU
- [RESUMO_INTEGRACAO.md](RESUMO_INTEGRACAO.md) - Integração Calculadora

---

## ✅ Checklist de Deploy

- [ ] Copiar .env.example para .env
- [ ] Configurar variáveis de ambiente
- [ ] Construir imagem Docker
- [ ] Subir container
- [ ] Verificar logs
- [ ] Testar acesso ao sistema
- [ ] Criar superusuário
- [ ] Testar Django admin
- [ ] Verificar migrations aplicadas
- [ ] Configurar backup de banco de dados

---

**Versão:** 1.0.0
**Data:** 2025-03-19
**Status:** ✅ Testado e funcional
