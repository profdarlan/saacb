# 🔧 COPIAR ARQUIVOS PARA O DOCKER - COMANDOS PRONTOS

## 🚨 Problema

Template não encontrado no container Docker.

---

## ✅ Copiar Todos os Arquivos de Uma Vez

Execute este bloco de comandos no terminal:

```bash
# 1. Criar estrutura de templates
docker exec -it saacb-django-teste mkdir -p /app/tarefas/templates/tarefas/integracao

# 2. Copiar templates de integração
docker cp /data/.openclaw/workspace-dev/projeto-saacb/tarefas/integracao/ saacb-django-teste:/app/tarefas/templates/tarefas/

# 3. Copiar views_integracao.py
docker cp /data/.openclaw/workspace-dev/projeto-saacb/tarefas/views_integracao.py saacb-django-teste:/app/tarefas/views_integracao.py

# 4. Copiar tarefa_detail.html (com botão de cálculo)
docker cp /data/.openclaw/workspace-dev/projeto-saacb/tarefas/templates/tarefas/tarefa_detail.html saacb-django-teste:/app/tarefas/templates/tarefas/tarefa_detail.html

# 5. Copiar admin.py (com botão no admin)
docker cp /data/.openclaw/workspace-dev/projeto-saacb/tarefas/admin.py saacb-django-teste:/app/tarefas/admin.py

# 6. Copiar models.py (com campos de integração)
docker cp /data/.openclaw/workspace-dev/projeto-saacb/tarefas/models.py saacb-django-teste:/app/tarefas/models.py

# 7. Copiar script fix-migrations.py
docker cp /data/.openclaw/workspace-dev/projeto-saacb/fix-migrations.py saacb-django-teste:/app/fix-migrations.py

# 8. Aplicar migrations
docker exec -it saacb-django-teste python fix-migrations.py

# 9. Reiniciar container
docker restart saacb-django-teste

# 10. Aguardar
sleep 10

# 11. Verificar logs
docker logs saacb-django-teste --tail 20
```

---

## ✅ Testar

```bash
curl http://192.168.1.51:30010/tarefas/tarefa/88/calcular/
```

Deve retornar HTML (sem erro).

---

**Copie e cole o bloco acima no terminal!** 🚀