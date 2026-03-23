# 📋 PLANO DE CORREÇÕES - SAACB

**Data:** 2026-03-21  
**Status:** 🔄 EM EXECUÇÃO

---

## 🎯 Objetivo

Implementar 5 correções e ajustes no sistema SAACB:

1. **Botão "Ver tabela completa dos créditos extraídos"** - Mostrar dados extraídos do PDF
2. **Relatório em PDF não está sendo gerado** - Corrigir função de geração de PDF
3. **Tabela editável após cálculo** - Criar tabela editável com resultados
4. **Erro admin "ERR_TIMED_OUT"** - Corrigir problema de SECURE_SSL_REDIRECT
5. **Remover módulo de cálculos do admin.py** - Remover `calcular_creditos_action`

---

## 📊 Análise Preliminar

### Arquivos a Serem Modificados

| Arquivo | Modificações | Status |
|---------|---------------|--------|
| `tarefas/views_integracao.py` | Remover função `calcular_link` | ⏳ |
| `tarefas/admin.py` | Remover função `calcular_creditos_action` | ⏳ |
| `tarefas/templates/tarefas/integracao/calcular_creditos.html` | Adicionar tabela editável | ⏳ |
| `projeto_saacb/settings_prod.py` | Verificar configurações | ⏳ |

### Arquivos a Serem Criados

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `tarefas/templates/tarefas/integracao/calcular_creditos_v2.html` | Nova versão com tabela editável | ⏳ |

---

## 🔧 Plano de Execução

### Etapa 1: Remover Módulo de Cálculos do Admin

**Arquivo:** `tarefas/admin.py`

**Ação:** Remover o método `calcular_creditos_action` da classe `TarefassamcAdmin`

**Justificativa:** O cálculo de créditos já está disponível na interface do usuário via `/tarefas/tarefa/<id>/calcular/`, não sendo necessário no admin.

---

### Etapa 2: Corrigir Erro "ERR_TIMED_OUT"

**Arquivo:** `projeto_saacb/settings_prod.py`

**Ação:** Verificar se `SECURE_SSL_REDIRECT=False` está definido adequadamente

**Justificativa:** O erro "ERR_TIMED_OUT" geralmente ocorre quando o Django tenta redirecionar para HTTPS, mas o Nginx não está configurado para isso.

---

### Etapa 3: Criar Nova Interface de Cálculo com Tabela Editável

**Arquivo:** `tarefas/templates/tarefas/integracao/calcular_creditos_v2.html`

**Ação:** Criar nova versão do template com:
- Tabela de resultados editável (inputs type="number")
- Função JavaScript para recalcular valores automaticamente
- Exportação para Excel editável

---

### Etapa 4: Corrigir Botão "Ver Tabela Completa"

**Arquivo:** `tarefas/templates/tarefas/integracao/calcular_creditos.html`

**Ação:** Verificar se o modal está sendo preenchido corretamente pelo JavaScript

**Causa provável:** O modal está sendo preenchido, mas o botão não está abrindo o modal corretamente

---

### Etapa 5: Corrigir Geração de PDF

**Arquivo:** `tarefas/views_integracao.py`

**Ação:** Verificar se a função de geração de PDF está funcionando corretamente

**Causa provável:** A função `baixar_relatorio_pdf` pode estar retornando um erro ou não sendo chamada

---

## 📝 Notas Importantes

### Sobre a Tabela Editável

O usuário quer que após o cálculo seja realizado, seja exibida uma tabela editável onde os valores podem ser ajustados manualmente. Esta tabela deve:

1. Mostrar todos os créditos calculados
2. Permitir edição do valor original
3. Permitir edição do índice de correção
4. Recalcular automaticamente os valores (valor corrigido = valor original × índice)
5. Permitir exportação para Excel com os valores editados

### Sobre o Erro ERR_TIMED_OUT

Este erro geralmente ocorre quando:

1. `SECURE_SSL_REDIRECT=True` no settings
2. O Nginx não está configurado para HTTPS
3. A aplicação tenta redirecionar para HTTPS, mas fica em loop timeout

**Solução:** Definir `SECURE_SSL_REDIRECT=False` no settings_prod.py

### Sobre Remoção do Módulo de Cálculos do Admin

O cálculo de créditos já está disponível na interface do usuário. O módulo no admin está redundante e pode ser removido.

---

## 🚀 Próximos Passos

1. Implementar Etapa 1: Remover módulo de cálculos do admin
2. Implementar Etapa 2: Corrigir erro ERR_TIMED_OUT
3. Implementar Etapa 3: Criar nova interface com tabela editável
4. Implementar Etapa 4: Corrigir botão "Ver Tabela Completa"
5. Implementar Etapa 5: Corrigir geração de PDF
6. Testar todas as funcionalidades
7. Criar documentação das alterações

---

## 📁 Arquivos de Documentação a Serem Criados

| Arquivo | Descrição |
|---------|-----------|
| `docs/CORRECOES_ETAPAS_20260321.md` | Documentação das correções implementadas |
| `docs/TABELA_EDITAVEL_GUIDE.md` | Guia da tabela editável |

---

**Versão:** 1.0  
**Data:** 2026-03-21  
**Status:** 🔄 PLANEJADO  
**Próximo:** INICIAR IMPLEMENTAÇÃO
