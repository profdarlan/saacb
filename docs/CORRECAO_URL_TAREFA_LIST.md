# 🔧 CORREÇÃO URL TAREFA_LIST - exibir_documento.html

## 🚨 Problema

```
NoReverseMatch at /tarefas/tarefa/88/gerar/despacho/
Reverse for 'tarefa_list' not found.
'tarefa_list' is not a valid view function or pattern name.
```

**Causa:** Template `exibir_documento.html` usando `{% url 'tarefa_list' %}` sem o namespace `tarefas:`.

---

## ✅ Solução Aplicada

### Arquivo: `tarefas/templates/tarefas/exibir_documento.html`

### Mudanças:

| Linha | Antes | Depois |
|-------|-------|--------|
| 14 | `{% url 'tarefa_list' %}` | `{% url 'tarefas:tarefa_list' %}` ✅ |
| 23 | `{% url 'tarefa_list' %}` | `{% url 'tarefas:tarefa_list' %}` ✅ |
| 63 | `{% url 'tarefa_detail' %}` | `{% url 'tarefas:tarefa_detail' %}` ✅ |

---

## 📋 Por que isso acontece?

O Django usa **namespaces** nas URLs para evitar conflitos quando o mesmo projeto tem múltiplas apps.

No arquivo `tarefas/urls.py`:
```python
app_name = 'tarefas'

urlpatterns = [
    path('', TarefaListView.as_view(), name='tarefa_list'),
    ...
]
```

Quando definimos `app_name = 'tarefas'`, todas as URLs precisam usar o namespace:
- ❌ Errado: `{% url 'tarefa_list' %}`
- ✅ Correto: `{% url 'tarefas:tarefa_list' %}`

---

## 🔄 Como Aplicar no Docker

### Método 1: Script Automático (Recomendado)

Execute no servidor 192.168.1.51:

```bash
cd /caminho/para/projeto_saacb

# Copiar template corrigido
docker cp ./tarefas/templates/tarefas/exibir_documento.html \
    saacb-django-teste:/app/tarefas/templates/tarefas/exibir_documento.html

# Reiniciar container
docker restart saacb-django-teste

# Aguardar
sleep 10

# Verificar logs
docker logs saacb-django-teste --tail 20
```

### Método 2: Manualmente

```bash
# 1. Copiar template corrigido
docker cp /caminho/para/projeto_saacb/tarefas/templates/tarefas/exibir_documento.html \
    saacb-django-teste:/app/tarefas/templates/tarefas/exibir_documento.html

# 2. Reiniciar container
docker restart saacb-django-teste

# 3. Aguardar 10 segundos
sleep 10

# 4. Verificar logs
docker logs saacb-django-teste --tail 20
```

---

## ✅ Esperado Após Correção

1. ✅ Acesso a `/tarefas/tarefa/<id>/gerar/despacho/` sem erro
2. ✅ Página de geração de documento carrega corretamente
3. ✅ Links de navegação funcionam
4. ✅ Botão "Voltar" redireciona corretamente

---

## 🔍 Verificação

Execute no servidor:

```bash
# 1. Verificar se o template foi atualizado
docker exec -it saacb-django-teste grep -c "tarefas:tarefa_list" /app/tarefas/templates/tarefas/exibir_documento.html

# Deve mostrar: 2

# 2. Verificar se não há mais 'tarefa_list' sem namespace
docker exec -it saacb-django-teste grep "url 'tarefa_list'" /app/tarefas/templates/tarefas/exibir_documento.html

# Deve mostrar nada

# 3. Testar acesso
curl http://192.168.1.51:30010/tarefas/tarefa/88/gerar/despacho/
```

---

## 🚨 Se o Erro Persistir

### Possível Causa 1: Template não foi atualizado

**Solução:** Verificar se o arquivo foi copiado corretamente
```bash
docker exec -it saacb-django-teste cat /app/tarefas/templates/tarefas/exibir_documento.html | grep "tarefas:tarefa_list"
```

### Possível Causa 2: Cache do Django

**Solução:** Reiniciar o container novamente
```bash
docker restart saacb-django-teste
```

### Possível Causa 3: Outros templates com mesmo erro

**Solução:** Verificar todos os templates
```bash
docker exec -it saacb-django-teste grep -r "url 'tarefa_list'" /app/tarefas/templates/
```

Se encontrar algum arquivo, precisa corrigir da mesma forma.

---

## 📝 Resumo da Correção

| Arquivo | Mudança |
|---------|---------|
| `exibir_documento.html` | `tarefa_list` → `tarefas:tarefa_list` (3 vezes) |

---

## 📚 Documentação Relacionada

- `CORRECAO_FINAL_TEMPLATE.md` - Correção do template path
- `CORRECAO_TEMPLATE_UPLOAD_PDF.md` - Correção template: upload + API porta 8002
- `ARQUIVOS_CORRIGIDOS.md` - Lista de arquivos corrigidos

---

**Versão:** 1.0.0
**Data:** 2025-03-20
**Status:** ✅ Correção aplicada
**Próximo:** Copiar para o Docker e testar
