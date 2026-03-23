# 🧮 Como Usar a Funcionalidade de Cálculos

## 🎯 Acessar pelo Django Admin

### 1. Acessar o Django Admin
```
http://192.168.1.51:30010/admin/
```

### 2. Ir em Tarefas
```
Tarefas → Tarefassamc
```

### 3. Ver o Botão de Cálculo

Na lista de tarefas, você verá uma coluna **"Calcular"** com o botão ⚡:

| ID | Tarefa | Nome | Usuário | Calcular |
|----|--------|------|---------|---------|
| 1 | 12345 | João Silva | admin | **⚡ Calcular** |

### 4. Clicar em "⚡ Calcular"

Isso abrirá a página de cálculo da tarefa.

---

## 🎯 Ações em Lote

### 1. Selecionar Tarefas

Marque as tarefas que deseja calcular:
- [ ] Tarefa 1
- [ ] Tarefa 2
- [ ] Tarefa 3

### 2. Escolher Ação

No menu suspenso de ações, selecione:
```
⚡ Calcular Créditos
```

### 3. Executar Ação

Clique em "Executar" e você verá uma lista com links para cada tarefa.

---

## 🎯 Acessar Diretamente pela URL

Você também pode acessar diretamente pela URL:

```
http://192.168.1.51:30010/tarefas/tarefa/<ID>/calcular/
```

Exemplo:
```
http://192.168.1.51:30010/tarefas/tarefa/1/calcular/
```

---

## 📊 Página de Cálculo

A página de cálculo mostra:

### 1. Informações da Tarefa
- 👤 Beneficiário (Nome e CPF)
- 💰 Benefício (NB1 e NB2)
- 📅 Competência (Data e período)
- 💵 Valor do débito

### 2. Status da API
- ✅ **Online** - API de cálculos disponível
- ❌ **Offline** - API de cálculos indisponível

### 3. Opções
- 📄 Checkbox: Gerar e salvar PDF do relatório

### 4. Botões
- ⚡ **Realizar Cálculo** - Executa o cálculo
- ← **Voltar** - Volta para detalhes da tarefa

---

## ✅ Após Calcular

Quando o cálculo é realizado, você verá:

### 1. Cards com Resultados

| Total Original | Total Corrigido | Diferença |
|--------------|----------------|-----------|
| R$ 6.533,33 | R$ 6.827,33 | R$ 294,00 |

### 2. Botões de Download

- 📄 **Baixar PDF** - Download do relatório em PDF
- 📊 **Baixar Excel** - Download da planilha em Excel

---

## 🔧 Campos Salvos no Banco

Após o cálculo, os seguintes campos são salvos na tarefa:

| Campo | Descrição |
|-------|-----------|
| `valor_original_calculado` | Valor original calculado |
| `valor_corrigido_calculado` | Valor corrigido calculado |
| `valor_diferenca` | Diferença calculada |
| `detalhes_calculo` | JSON com detalhes completos |
| `relatorio_pdf` | Arquivo PDF do relatório |
| `calculado_em` | Data/hora do cálculo |

---

## 📝 Exemplo de Uso

### Passo 1: Criar uma Tarefa

```
1. Acesse /admin/
2. Tarefassamc → + Adicionar Tarefassamc
3. Preencha os dados:
   - Nome: João Silva
   - CPF: 123.456.789-00
   - NB1: 1247744709
   - Competência: 2002-07-01
   - Valor: 6.533,33
4. Salvar
```

### Passo 2: Calcular Créditos

```
1. Na lista de tarefas, clique em "⚡ Calcular"
2. A página de cálculo abrirá
3. Clique em "⚡ Realizar Cálculo"
4. Aguarde o resultado
5. Veja os cards com os resultados
```

### Passo 3: Baixar Relatórios

```
1. Na página de resultado, clique em:
   - "📄 Baixar PDF" para relatório PDF
   - "📊 Baixar Excel" para planilha
2. Os arquivos serão baixados
```

---

## 🔄 Recalcular

Para recalcular uma tarefa:

1. Acesse a página de cálculo novamente
2. Clique em "⚡ Realizar Cálculo"
3. Os novos resultados substituirão os antigos

---

## 🔍 Ver Resultados Anteriores

Para ver o cálculo anterior de uma tarefa:

1. Acesse a tarefa no Django Admin
2. Role até os campos de integração
3. Você verá:
   - Valor Original Calculado
   - Valor Corrigido Calculado
   - Diferença Calculada
   - Data do Cálculo

---

## ⚠️ Erros Comuns

### Erro: "API de cálculos indisponível"

**Solução:**
```bash
# Verificar se a API está rodando
curl http://192.168.1.51:8002/

# Se não estiver, iniciá-la
cd /data/.openclaw/workspace-dev/planilha_saacb
uvicorn main:app --host 0.0.0.0 --port 8002
```

### Erro: "Nenhum índice configurado"

**Solução:**
Acesse http://192.168.1.51:8002 e configure os índices de correção.

---

## 📚 URLs Úteis

| URL | Descrição |
|-----|-----------|
| `/admin/` | Django Admin |
| `/admin/tarefas/tarefassamc/` | Lista de tarefas |
| `/tarefas/tarefa/<ID>/calcular/` | Página de cálculo |
| `/tarefas/tarefa/<ID>/pdf/` | Download PDF |
| `/tarefas/tarefa/<ID>/excel/` | Download Excel |

---

**Versão:** 1.0.0
**Data:** 2025-03-19
**Status:** ✅ Funcional
