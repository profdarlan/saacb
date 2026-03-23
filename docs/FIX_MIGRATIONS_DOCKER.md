# 🔧 CORREÇÃO MIGRATIONS - SAACB DOCKER

## 🚨 Erro Atual

```
OperationalError at /tarefas/
no such column: tarefas_tarefassamc.valor_original_calculado
```

**Container:** `saacb-django-teste`
**Porta:** 30010

---

## ✅ Solução Rápida

### Passo 1: Executar Script de Correção

```bash
# Entrar no container
docker exec -it saacb-django-teste bash

# Executar correção
python fix-migrations.py

# Sair
exit
```

### Passo 2: Reiniciar Container

```bash
# Reiniciar o container
docker restart saacb-django-teste

# OU via docker-compose
docker-compose restart saacb
```

### Passo 3: Verificar

```bash
# Testar acesso
curl http://192.168.1.51:30010/tarefas/

# Deve funcionar sem erro
```

---

## 🔄 Comando Único

```bash
docker exec -it saacb-django-teste python fix-migrations.py && docker restart saacb-django-teste
```

---

## 📋 Se Ainda Der Erro

### Opção 1: Recriar Container

```bash
cd /data/.openclaw/workspace-dev/projeto-saacb

# Parar e remover
docker-compose down

# Reconstruir
docker-compose build

# Subir
docker-compose up -d
```

### Opção 2: Aplicar Migrations Manualmente

```bash
# Entrar no container
docker exec -it saacb-django-teste bash

# Aplicar todas as migrations
python manage.py migrate --noinput

# Sair
exit

# Reiniciar
docker restart saacb-django-teste
```

### Opção 3: Fake Migration

```bash
# Entrar no container
docker exec -it saacb-django-teste bash

# Fake migration se o banco já estiver ok
python manage.py migrate tarefas 0015_integracao_calculadora --fake

# Sair
exit

# Reiniciar
docker restart saacb-django-teste
```

---

## 🔍 Verificar Migrations Aplicadas

```bash
docker exec -it saacb-django-teste python manage.py showmigrations tarefas
```

Deve mostrar:
```
tarefas
 [X] 0001_initial
 [X] 0002_role_userprofile
 ...
 [X] 0015_integracao_calculadora  ← Esta deve estar marcada
```

---

## 📊 Status do Container

```bash
# Ver se está rodando
docker ps | grep saacb

# Ver logs
docker logs saacb-django-teste --tail 50

# Ver logs completos
docker logs -f saacb-django-teste
```

---

## ✅ Esperado Após Correção

- ✅ Acesso a `/tarefas/` sem erro
- ✅ Migration `0015_integracao_calculadora` aplicada
- ✅ Colunas de integração presentes no banco

---

**Nome do Container:** `saacb-django-teste`
**Porta:** 30010
**Projeto:** `projeto-saacb` (com hífen)
