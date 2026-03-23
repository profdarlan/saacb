# 🔧 CORREÇÃO: NoReverseMatch em /tarefas/tarefa/88/calcular/

**Data:** 2026-03-21  
**Status:** ✅ CORRIGIDO

---

## 🐛 Descrição do Erro

### Erro
```
NoReverseMatch at /tarefas/tarefa/88/calcular/
Reverse for 'detail' not found. 'detail' is not a valid view function or pattern name.
```

### Stack Trace
```
File "/app/tarefas/views_integracao.py", line 92, in calcular_creditos_tarefa
    return redirect('tarefas:detail', tarefa_id=tarefa.id)
```

### URLs Afetadas
- `/tarefas/tarefa/<id>/calcular/`
- `/tarefas/tarefa/<id>/pdf/`
- `/tarefas/tarefa/<id>/excel/`

---

## 🔍 Análise do Problema

### Causa Raiz
O arquivo `tarefas/views_integracao.py` estava tentando resolver a URL `'tarefas:detail'`, mas o nome correto configurado em `tarefas/urls.py` é `'tarefa_detail'`.

### Arquivos Envolvidos

**1. `tarefas/urls.py`** (URLs corretas)
```python
app_name = 'tarefas'

urlpatterns = [
    path('<int:pk>/', TarefaDetailView.as_view(), name='tarefa_detail'),  # ← Nome correto
    # ... outras URLs
]
```

**2. `tarefas/views_integracao.py`** (Errado)
```python
# ❌ ERRADO - Nome da URL incorreto
return redirect('tarefas:detail', tarefa_id=tarefa.id)

# ✅ CORRETO - Nome da URL correto
return redirect('tarefas:tarefa_detail', tarefa_id=tarefa.id)
```

### Locais da Correção
Foram encontradas **5 ocorrências** do erro no arquivo:

| Linha | Função | Correção |
|-------|--------|----------|
| 92 | `calcular_creditos_tarefa` | ✅ Corrigido |
| 180 | `calcular_ajax` (erro) | ✅ Corrigido |
| 210 | `baixar_relatorio_pdf` | ✅ Corrigido |
| 223 | `baixar_relatorio_excel` | ✅ Corrigido |
| 253 | `status_api` (erro) | ✅ Corrigido |

---

## ✅ Soluções Aplicadas

### 1. Restauração do Arquivo Original

O arquivo `views_integracao.py` estava **gravemente corrompido** com:
- Linhas duplicadas
- Erros de sintaxe
- Imports quebrados

**Comando executado:**
```bash
cd projeto-saacb
git checkout 72899f4 -- tarefas/views_integracao.py
```

### 2. Correção dos Nomes de URL

**Comando executado:**
```bash
cd projeto-saacb
sed -i "s/'tarefas:detail'/'tarefas:tarefa_detail'/g" tarefas/views_integracao.py
```

**Resultado:** 5 ocorrências corrigidas

---

## 📋 URLs Corretas para Referência

| Nome da URL | Padrão | Uso Correto |
|-------------|--------|-------------|
| `tarefas:tarefa_list` | `/tarefas/` | `{% url 'tarefas:tarefa_list' %}` |
| `tarefas:tarefa_detail` | `/tarefas/<pk>/` | `{% url 'tarefas:tarefa_detail' pk=tarefa.id %}` |
| `tarefas:integracao_calcular_creditos` | `/tarefas/tarefa/<tarefa_id>/calcular/` | `{% url 'tarefas:integracao_calcular_creditos' tarefa.id %}` |
| `tarefas:integracao_baixar_pdf` | `/tarefas/tarefa/<tarefa_id>/pdf/` | `redirect('tarefas:integracao_baixar_pdf', tarefa_id=tarefa.id)` |
| `tarefas:integracao_baixar_excel` | `/tarefas/tarefa/<tarefa_id>/excel/` | `redirect('tarefas:integracao_baixar_excel', tarefa_id=tarefa.id)` |

---

## 🧪 Verificação

### Comandos para Verificar

```bash
# 1. Verificar se as URLs existem
cd projeto-saacb
python manage.py show_urls | grep tarefa_detail

# 2. Testar o reverse no Django shell
python manage.py shell
>>> from django.urls import reverse
>>> reverse('tarefas:tarefa_detail', kwargs={'pk': 88})
'/tarefas/88/'

# 3. Verificar o arquivo corrigido
grep -c "tarefas:tarefa_detail" tarefas/views_integracao.py
# Deve retornar: 5
```

---

## 📝 Notas Importantes

### 1. Namespace do App
O app `tarefas` tem um namespace definido (`app_name = 'tarefas'`), então **todas** as URLs devem ser referenciadas com o prefixo `tarefas:`.

### 2. Parâmetro da URL
A URL `tarefa_detail` usa `<int:pk>` (não `tarefa_id`), então ao fazer o redirect:

```python
# ✅ CORRETO
return redirect('tarefas:tarefa_detail', pk=tarefa.id)

# ❌ ERRADO
return redirect('tarefas:tarefa_detail', tarefa_id=tarefa.id)
return redirect('tarefas:tarefa_detail', tarefa.id)
```

### 3. Prevenção Futura
Para evitar erros similares:

1. **Sempre verificar** o nome correto da URL em `urls.py` antes de usar `redirect()` ou `reverse()`
2. **Usar o Django shell** para testar: `reverse('nome:url')`
3. **Documentar** URLs em um arquivo centralizado (como `MAPEAMENTO_SISTEMA_IA.md`)

---

## 🚀 Deploy

### Aplicar a Correção em Produção

```bash
# 1. Fazer pull das mudanças
cd /DATA/AppData/fitt/projeto-saacb
git pull

# 2. Verificar se o arquivo foi atualizado
grep -c "tarefas:tarefa_detail" tarefas/views_integracao.py

# 3. Reiniciar o container Docker
docker restart saacb-django-teste

# 4. Verificar logs
docker logs saacb-django-teste --tail 50

# 5. Testar a URL afetada
curl http://192.168.1.51:30010/tarefas/tarefa/88/calcular/
```

---

## 📚 Referências

- **Arquivo:** `tarefas/views_integracao.py`
- **Arquivo:** `tarefas/urls.py`
- **Documentação:** Django URL Dispatch - https://docs.djangoproject.com/en/4.2/topics/http/urls/
- **Mapeamento do Sistema:** `MAPEAMENTO_SISTEMA_IA.md`

---

**Versão:** 1.0  
**Data:** 2026-03-21  
**Status:** ✅ CORRIGIDO  
**Próximo:** Fazer deploy em produção
