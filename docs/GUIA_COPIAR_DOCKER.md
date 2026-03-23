# 🔧 COPIAR ARQUIVOS PARA O DOCKER - GUIA MANUAL

## 🚨 Problema

```
TemplateDoesNotExist at /tarefas/tarefa/88/calcular/
tarefas/calcular_creditos.html
```

**Causa:** Arquivos de integração não estão no container Docker.

---

## ✅ Solução: Copiar Arquivos para o Docker

### Método 1: Script Automático (Recomendado)

```bash
cd /data/.openclaw/workspace-dev/projeto-saacb

# Dar permissão e executar
chmod +x copiar-para-docker.sh
./copiar-para-docker.sh
```

O script copiará:
1. ✅ `fix-migrations.py`
2. ✅ Templates de integração (`tarefas/templates/tarefas/integracao/`)
3. ✅ `views_integracao.py`
4. ✅ `models.py` atualizado
5. ✅ `admin.py` atualizado
6. ✅ `tarefa_detail.html` atualizado
7. ✅ Reiniciará o container

---

### Método 2: Manualmente Passo a Passo

Execute estes comandos no terminal:

#### Passo 1: Copiar script fix-migrations.py
```bash
docker cp /data/.openclaw/workspace-dev/projeto-saacb/fix-migrations.py \
    saacb-django-teste:/app/fix-migrations.py
```

#### Passo 2: Criar estrutura de templates no container
```bash
docker exec -it saacb-django-teste mkdir -p /app/tarefas/templates/tarefas/integracao
```

#### Passo 3: Copiar templates de integração
```bash
docker cp /data/.openclaw/workspace-dev/projeto-saacb/tarefas/integracao/ \
    saacb-django-teste:/app/tarefas/templates/tarefas/
```

#### Passo 4: Copiar views_integracao.py
```bash
docker cp /data/.openclaw/workspace-dev/projeto-saacb/tarefas/views_integracao.py \
    saacb-django-teste:/app/tarefas/views_integracao.py
```

#### Passo 5: Copiar models.py atualizado
```bash
docker cp /data/.openclaw/workspace-dev/projeto-saacb/tarefas/models.py \
    saacb-django-teste:/app/tarefas/models.py
```

#### Passo 6: Copiar admin.py atualizado
```bash
docker cp /data/.openclaw/workspace-dev/projeto-saacb/tarefas/admin.py \
    saacb-django-teste:/app/tarefas/admin.py
```

#### Passo 7: Copiar tarefa_detail.html atualizado
```bash
docker cp /data/.openclaw/workspace-dev/projeto-saacb/tarefas/templates/tarefas/tarefa_detail.html \
    saacb-django-teste:/app/tarefas/templates/tarefas/tarefa_detail.html
```

#### Passo 8: Reiniciar o container
```bash
docker restart saacb-django-teste
```

---

### Método 3: Via docker-compose (Reconstruir Imagem)

```bash
cd /data/.openclaw/workspace-dev/projeto-saacb

# Parar e remover
docker-compose down

# Reconstruir imagem (copia todos os arquivos)
docker-compose build

# Subir novo container
docker-compose up -d

# Verificar logs
docker-compose logs -f
```

---

## 📋 Verificação

### 1. Verificar templates no container
```bash
docker exec -it saacb-django-teste ls -la /app/tarefas/templates/tarefas/integracao/
```

Deve mostrar:
```
calcular_creditos.html
```

### 2. Verificar se o template existe
```bash
docker exec -it saacb-django-teste cat /app/tarefas/templates/tarefas/integracao/calcular_creditos.html
```

Deve mostrar o conteúdo do template HTML.

### 3. Verificar views_integracao.py
```bash
docker exec -it saacb-django-teste ls -la /app/tarefas/views_integracao.py
```

### 4. Testar acesso à página de cálculo
```bash
curl http://192.168.1.51:30010/tarefas/tarefa/88/calcular/
```

Deve retornar HTML (não erro).

---

## 🚨 Troubleshooting

### Erro: "docker: command not found"

**Solução:** O Docker não está no PATH.
```bash
# Adicionar Docker ao PATH (Linux/Mac)
export PATH=$PATH:/usr/bin

# Ou usar caminho completo
/usr/bin/docker cp ...
```

### Erro: "No such file or directory"

**Solução:** O arquivo não existe no host.
```bash
# Verificar se o arquivo existe no host
ls -la /data/.openclaw/workspace-dev/projeto-saacb/tarefas/integracao/
```

### Erro: "Permission denied"

**Solução:** Dar permissão ao script.
```bash
chmod +x copiar-para-docker.sh
```

### Erro: Template ainda não encontrado

**Solução:** Verificar se foi copiado para o lugar certo.
```bash
docker exec -it saacb-django-teste find /app -name "calcular_creditos.html"
```

---

## 📝 Resumo dos Arquivos para Copiar

| Arquivo no Host | Local no Container | Finalidade |
|----------------|------------------|-----------|
| `fix-migrations.py` | `/app/fix-migrations.py` | Corrigir migrations |
| `tarefas/integracao/` | `/app/tarefas/templates/tarefas/integracao/` | Templates cálculo |
| `views_integracao.py` | `/app/tarefas/views_integracao.py` | Views cálculo |
| `models.py` | `/app/tarefas/models.py` | Modelos com campos novos |
| `admin.py` | `/app/tarefas/admin.py` | Admin com botão cálculo |
| `tarefa_detail.html` | `/app/tarefas/templates/tarefas/tarefa_detail.html` | Detalhes com botão cálculo |

---

## ✅ Após Copiar os Arquivos

### 1. Aplicar migrations
```bash
docker exec -it saacb-django-teste python fix-migrations.py
```

### 2. Reiniciar container
```bash
docker restart saacb-django-teste
```

### 3. Testar
```bash
curl http://192.168.1.51:30010/tarefas/
curl http://192.168.1.51:30010/tarefas/tarefa/88/calcular/
```

### 4. Acessar no navegador
```
http://192.168.1.51:30010/tarefas/tarefa/88/calcular/
```

---

## 🎯 Ordem Recomendada

1. ✅ Executar `copiar-para-docker.sh` (ou Método 2 manual)
2. ✅ Executar `fix-migrations.py` no container
3. ✅ Reiniciar container
4. ✅ Testar acesso

---

**Versão:** 1.0.0
**Data:** 2025-03-19
**Status:** ✅ Guia completo
