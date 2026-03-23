# 🔧 CORREÇÃO: NoReverseMatch - Parâmetro Errado no redirect()

**Data:** 2026-03-21  
**Status:** ✅ CORRIGIDO

---

## 🐛 Descrição do Erro

### Erro
```
NoReverseMatch at /tarefas/tarefa/88/calcular/
Reverse for 'tarefa_detail' with keyword arguments '{'tarefa_id': 88}' not found. 
1 pattern(s) tried: ['tarefas/(?P<pk>[0-9]+)/\Z']
```

### Stack Trace
```
File "/app/tarefas/views_integracao.py", line 92, in calcular_creditos_tarefa
    return redirect('tarefas:tarefa_detail', tarefa_id=tarefa.id)
```

---

## 🔍 Análise do Problema

### Causa Raiz

A URL `tarefa_detail` no `urls.py` usa `<int:pk>`:

```python
path('<int:pk>/', TarefaDetailView.as_view(), name='tarefa_detail'),
```

Mas o `redirect()` estava passando `tarefa_id=` em vez de `pk=`:

```python
# ❌ ERRADO
return redirect('tarefas:tarefa_detail', tarefa_id=tarefa.id)
```

### Por que isso falha?

- A URL espera um parâmetro chamado `pk`
- Mas o redirect está passando um parâmetro chamado `tarefa_id`
- Django não consegue encontrar o valor de `pk` e lança NoReverseMatch

---

## ✅ Solução Aplicada

### Comando Executado

```bash
cd projeto-saacb
sed -i "s/redirect('tarefas:tarefa_detail', tarefa_id=tarefa.id)/redirect('tarefas:tarefa_detail', pk=tarefa.id)/g" tarefas/views_integracao.py
```

### Correção

**Antes:**
```python
return redirect('tarefas:tarefa_detail', tarefa_id=tarefa.id)  # ❌ ERRO
```

**Depois:**
```python
return redirect('tarefas:tarefa_detail', pk=tarefa.id)  # ✅ CORRETO
```

### Locais Corrigidos

| Linha | Função | Status |
|-------|--------|--------|
| 92 | `calcular_creditos_tarefa` | ✅ Corrigido |
| 180 | `calcular_ajax` (erro tratado) | ✅ Corrigido |
| 210 | `baixar_relatorio_pdf` | ✅ Corrigido |
| 223 | `baixar_relatorio_excel` | ✅ Corrigido |
| 253 | `status_api` (erro tratado) | ✅ Corrigido |

**Total:** 5 ocorrências corrigidas

---

## 🧪 Testes Realizados

### 1. Django Check

```bash
python manage.py check
# Resultado: System check identified no issues (0 silenced) ✅
```

### 2. Teste de Reverse

```python
from django.urls import reverse

# ✅ CORRETO
url = reverse('tarefas:tarefa_detail', kwargs={'pk': 88})
# Resultado: /tarefas/88/

# ❌ ERRADO (esperado falhar)
url = reverse('tarefas:tarefa_detail', kwargs={'tarefa_id': 88})
# Resultado: NoReverseMatch
```

---

## 📋 Checklist de Prevenção

### Ao fazer redirect() para URLs com parâmetros

**1. Verificar a definição da URL:**

```python
# Em urls.py
path('<int:pk>/', View.as_view(), name='nome_url'),  # ← parâmetro é 'pk'
```

**2. Usar o mesmo nome do parâmetro no redirect():**

```python
# ✅ CORRETO
return redirect('app:nome_url', pk=objeto.id)

# ❌ ERRADO
return redirect('app:nome_url', id=objeto.id)  # Nome diferente!
return redirect('app:nome_url', obj_id=objeto.id)  # Nome diferente!
```

### Padrão de Nomes de Parâmetros Django

| Nome comum | Descrição |
|------------|-----------|
| `pk` | Primary Key (mais comum) |
| `id` | ID genérico |
| `slug` | Slug para URLs amigáveis |
| `tarefa_id`, `user_id`, etc. | Nomes específicos (devem bater com a URL) |

**Importante:** O nome no `redirect()` DEVE bater exatamente com o nome definido na `path()`!

---

## 🚀 Deploy

### Aplicar em Produção

```bash
cd /DATA/AppData/fitt/projeto-saacb

# 1. Fazer pull das alterações
git pull

# 2. Verificar se o arquivo foi atualizado
grep -c "tarefas:tarefa_detail.*pk=" tarefas/views_integracao.py
# Deve retornar: 5

# 3. Reiniciar o container Docker
docker restart saacb-django-teste

# 4. Verificar logs
docker logs saacb-django-teste --tail 50

# 5. Testar a URL
curl http://192.168.1.51:30010/tarefas/tarefa/88/calcular/ -X POST
```

---

## 📝 Lições Aprendidas

### 1. Erro comum de NoReverseMatch

O erro `NoReverseMatch` geralmente indica:
1. Nome da URL errado (já corrigido anteriormente)
2. Parâmetro errado no `reverse()` (este caso)

### 2. Sempre verificar a definição da URL

Antes de usar `reverse()` ou `redirect()`:
1. Olhar a definição em `urls.py`
2. Verificar o nome do parâmetro (`<int:pk>`, `<int:tarefa_id>`, etc.)
3. Usar o mesmo nome no `reverse()`/`redirect()`

### 3. Testar no Django Shell

```bash
python manage.py shell

>>> from django.urls import reverse
>>> reverse('app:url_name', kwargs={'pk': 123})
'/app/123/'
```

---

## 📚 Referências

- **Arquivo:** `tarefas/views_integracao.py`
- **Arquivo:** `tarefas/urls.py`
- **Documentação:** Django URL Dispatcher - https://docs.djangoproject.com/en/4.2/topics/http/urls/
- **Mapeamento do Sistema:** `docs/MAPEAMENTO_SISTEMA_IA.md`

---

## 🔄 Histórico de Correções da URL

| Data | Erro | Solução | Documentação |
|------|------|---------|-------------|
| 2026-03-21 | `'tarefas:detail'` não existe | Alterado para `'tarefas:tarefa_detail'` | `docs/CORRECAO_NOREVERSMATCH_20260321.md` |
| 2026-03-21 | Parâmetro `tarefa_id=` errado | Alterado para `pk=` | Este arquivo |

---

**Versão:** 1.0  
**Data:** 2026-03-21  
**Status:** ✅ CORRIGIDO  
**Próximo:** Fazer deploy em produção
