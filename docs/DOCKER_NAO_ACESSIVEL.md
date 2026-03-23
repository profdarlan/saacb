# 🚨 DOCKER NÃO ACESSÍVEL NO WORKSPACE

## Problema

O Docker **não está disponível** no ambiente `/data/.openclaw/workspace-dev/`.

O Docker está rodando no servidor **192.168.1.51**, mas eu não tenho acesso a ele através deste workspace.

---

## ✅ Solução: Executar Comandos no Servidor

Você precisa executar os comandos **diretamente no servidor** onde o Docker está rodando (192.168.1.51).

### 1. Conectar ao Servidor

```bash
ssh usuario@192.168.1.51
```

### 2. Ir até o Diretório do Projeto

```bash
cd /caminho/para/projeto-saacb
# ou
cd /data/projetos/projeto-saacb
```

### 3. Executar os Comandos de Copiar

Copie e cole o bloco de comandos do arquivo `COMANDOS_COPIAR_DOCKER.md`:

```bash
# 1. Criar estrutura
docker exec -it saacb-django-teste mkdir -p /app/tarefas/templates/tarefas/integracao

# 2. Copiar templates
docker cp ./tarefas/integracao/ saacb-django-teste:/app/tarefas/templates/tarefas/

# 3. Copiar views
docker cp ./tarefas/views_integracao.py saacb-django-teste:/app/tarefas/views_integracao.py

# 4. Copiar templates atualizados
docker cp ./tarefas/templates/tarefas/tarefa_detail.html saacb-django-teste:/app/tarefas/templates/tarefas/tarefa_detail.html

# 5. Copiar admin atualizado
docker cp ./tarefas/admin.py saacb-django-teste:/app/tarefas/admin.py

# 6. Copiar models atualizado
docker cp ./tarefas/models.py saacb-django-teste:/app/tarefas/models.py

# 7. Copiar script de correção
docker cp ./fix-migrations.py saacb-django-teste:/app/fix-migrations.py

# 8. Aplicar migrations
docker exec -it saacb-django-teste python fix-migrations.py

# 9. Reiniciar
docker restart saacb-django-teste
```

### 4. Verificar se Funcionou

```bash
# Verificar container
docker ps | grep saacb

# Verificar logs
docker logs saacb-django-teste --tail 50

# Testar acesso
curl http://192.168.1.51:30010/tarefas/
```

---

## 📋 Alternativa: Reconstruir Imagem

Se os comandos acima não funcionarem, reconstrua a imagem do zero:

```bash
# 1. Parar container
docker stop saacb-django-teste

# 2. Remover container
docker rm saacb-django-teste

# 3. Reconstruir imagem
cd /caminho/para/projeto-saacb
docker-compose build

# 4. Subir novo container
docker-compose up -d

# 5. Verificar logs
docker-compose logs -f saacb
```

---

## 🔍 Verificar Arquivos

Antes de copiar, verifique se os arquivos existem no servidor:

```bash
ls -la tarefas/integracao/
ls -la tarefas/views_integracao.py
ls -la fix-migrations.py
```

---

## 📋 Resumo do Problema

| Aspecto | Status |
|---------|--------|
| Docker no workspace-dev | ❌ Não disponível |
| Docker no servidor 192.168.1.51 | ✅ Rodando (você acessa) |
| Arquivos em projeto-saacb | ✅ Criados aqui |
| Necessário copiar para Docker | ⚠️ Você deve fazer |

---

## ✅ Próximos Passos

1. **Conectar ao servidor** via SSH
2. **Copiar arquivos** usando os comandos acima
3. **Aplicar migrations** com `fix-migrations.py`
4. **Reiniciar container**
5. **Testar acesso** ao sistema

---

**Importante:** Os arquivos de integração foram criados em `/data/.openclaw/workspace-dev/projeto-saacb/`, mas precisam ser copiados para o Docker no servidor onde o container está rodando.

**Versão:** 1.0.0
**Data:** 2025-03-19
**Status:** ⚠️ Requer acesso ao servidor Docker
