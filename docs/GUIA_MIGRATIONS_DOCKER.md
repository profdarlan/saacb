# 🔧 APPLIAR MIGRATIONS DOCKER - GUIA PASSO A PASSO

## 🚨 Problema Atual

```
OperationalError at /tarefas/
no such column: tarefas_tarefassamc.valor_original_calculado
```

**Causa:** Migration `0015_integracao_calculadora` não foi executada no banco do Docker.

---

## ✅ Solução: Aplicar Migrations no Docker

### Método 1: Script Automático (Recomendado)

```bash
cd /data/.openclaw/workspace-dev/projeto-saacb

# Dar permissão ao script
chmod +x aplicar-migrations-docker.sh

# Executar script
./aplicar-migrations-docker.sh
```

O script fará:
1. ✅ Verificar se o container está rodando
2. ✅ Copiar script de correção para o container
3. ✅ Aplicar todas as migrations
4. ✅ Verificar se a migration de integração foi aplicada
5. ✅ Reiniciar o container
6. ✅ Mostrar logs iniciais

---

### Método 2: Manualmente Passo a Passo

#### Passo 1: Verificar se o container está rodando
```bash
docker ps | grep saacb-django-teste
```

Se não estiver rodando:
```bash
docker start saacb-django-teste
# ou
docker-compose up -d
```

#### Passo 2: Copiar o script de correção para o container
```bash
docker cp /data/.openclaw/workspace-dev/projeto-saacb/fix-migrations.py \
    saacb-django-teste:/app/fix-migrations.py
```

#### Passo 3: Aplicar migrations
```bash
docker exec -it saacb-django-teste python manage.py migrate
```

Você deve ver algo como:
```
Operations to perform:
  Apply all migrations: tarefas
Running migrations:
  Applying tarefas.0015_integracao_calculadora... OK
```

#### Passo 4: Verificar migrations aplicadas
```bash
docker exec -it saacb-django-teste python manage.py showmigrations tarefas
```

Procure por:
```
[X] 0015_integracao_calculadora
```

#### Passo 5: Reiniciar o container
```bash
docker restart saacb-django-teste
```

#### Passo 6: Aguardar o container iniciar
```bash
sleep 10
```

#### Passo 7: Testar o acesso
```bash
curl http://192.168.1.51:30010/tarefas/
```

Deve retornar HTML sem erros.

---

### Método 3: Fake Migration (Se o banco já estiver ok)

Se as migrations já tiverem sido aplicadas mas o Django não souber:

```bash
docker exec -it saacb-django-teste python manage.py migrate \
    tarefas 0015_integracao_calculadora --fake
```

---

### Método 4: Recriar o Container (Última Recurso)

Se nada funcionar, recrie o container:

```bash
cd /data/.openclaw/workspace-dev/projeto-saacb

# Parar e remover
docker-compose down

# Remover volume de banco (ATENÇÃO: apaga os dados)
docker volume rm projeto-saacb_data 2>/dev/null || echo "Volume não existe"

# Reconstruir imagem
docker-compose build

# Subir novo container
docker-compose up -d

# Verificar logs
docker-compose logs -f saacb
```

---

## 🔍 Verificar se Funcionou

### 1. Verificar migrations aplicadas
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

### 2. Verificar se o sistema funciona
```bash
curl http://192.168.1.51:30010/tarefas/
```

Deve retornar HTML (não erro).

### 3. Acessar no navegador
```
http://192.168.1.51:30010/tarefas/
```

Deve carregar a lista de tarefas sem erro.

---

## 🚨 Troubleshooting

### Erro: "docker exec: container not running"

**Solução:**
```bash
docker start saacb-django-teste
```

### Erro: "Permission denied"

**Solução:**
```bash
chmod +x aplicar-migrations-docker.sh
```

### Erro: "Database locked"

**Solução:**
```bash
docker restart saacb-django-teste
# Aguardar 10 segundos
# Tentar novamente
```

### Erro: "No module named 'fix-migrations'"

**Solução:**
O script deve ser executado assim:
```bash
docker exec -it saacb-django-teste python fix-migrations.py
```

### Erro persiste após aplicar migrations

**Solução:**
Recriar o container (Método 4 acima).

---

## 📋 Checklist

- [ ] Container está rodando
- [ ] Script fix-migrations.py copiado para o container
- [ ] Migrations aplicadas (`python manage.py migrate`)
- [ ] Migration 0015_integracao_calculadora marcada como aplicada
- [ ] Container reiniciado
- [ ] Acesso a `/tarefas/` sem erro
- [ ] Botão "⚡ Calcular" visível na lista de tarefas
- [ ] Botão "⚡ Calcular Créditos" visível na página de detalhes

---

## 📚 Comandos Úteis

### Docker
```bash
# Ver containers rodando
docker ps | grep saacb

# Ver logs do container
docker logs saacb-django-teste --tail 50

# Logs em tempo real
docker logs -f saacb-django-teste

# Entrar no container
docker exec -it saacb-django-teste bash

# Reiniciar container
docker restart saacb-django-teste

# Parar container
docker stop saacb-django-teste
```

### Django (dentro do container)
```bash
# Ver migrations
python manage.py showmigrations

# Aplicar migrations
python manage.py migrate

# Verificar sistema
python manage.py check

# Django shell
python manage.py shell
```

---

## ✅ Esperado Após Correção

1. ✅ Acesso a `/tarefas/` sem erro
2. ✅ Migration `0015_integracao_calculadora` aplicada
3. ✅ Colunas de integração no banco de dados
4. ✅ Botão "⚡ Calcular" visível no admin
5. ✅ Botão "⚡ Calcular Créditos" visível na página de detalhes

---

**Versão:** 1.0.0
**Data:** 2025-03-19
**Status:** ✅ Guia completo e testado
