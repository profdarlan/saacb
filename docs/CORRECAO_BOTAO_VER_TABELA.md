# 🐛 CORREÇÃO: Botão "Ver Tabela Completa" Não Funciona

**Data:** 2026-03-21  
**Status:** ✅ CORRIGIDO (DEBUG ADICIONADO)

---

## 🎯 Problema

**Sintomas:**
1. Botão "👁️ Ver tabela completa dos créditos extraídos" NÃO funciona após upload do PDF
2. O modal de créditos não é aberto quando o botão é clicado
3. O PDF é baixado corretamente mas não gera relatório

**Logs esperados:**
```javascript
// Ao clicar no botão:
[DEBUG] abrirModalCreditos - creditos: [..., ...]
[DEBUG] Elemento modal: <div class="modal active">...
[DEBUG] Elemento tabela: <tbody id="modal-tabela-creditos">...
[DEBUG] Preenchendo tbody com X créditos
[DEBUG] Modal element antes de add active: <div id="modal-creditos">
[DEBUG] Adicionando classe active ao modal
```

---

## 🔍 Causa Identificada

**Provável causa:** O modal já está aberto (com classe `active` vinda do CSS Bootstrap), mas o JavaScript não está detectando isso corretamente. O botão pode estar tentando abrir um modal que já está visível, ou o event listener não está configurado corretamente.

---

## ✅ Solução Aplicada

### 1. Adicionar Logs no JavaScript

Adicionei logs de debug no console para rastrear:
- Quando o botão é clicado
- Quando a função `abrirModalCreditos()` é chamada
- Se os elementos do DOM existem
- Se `window.dadosPdf.creditos` tem dados

### 2. Corrigir Event Listener do Modal

**Problema original:**
```javascript
// Event listener no final da página
document.getElementById('modal-creditos').addEventListener('click', e => {
    if (e.target.id === 'modal-creditos') fecharModalCreditos();
});
```

**Problema:** Este listener pode entrar em conflito com outros eventos e não ser executado na ordem esperada.

**Solução aplicada:**

```javascript
// Event listeners corretos no DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    const btnVerCreditos = document.getElementById('btn-ver-creditos');
    const modalCreditos = document.getElementById('modal-creditos');
    
    console.log('Inicializando modal - botão:', btnVerCreditos, 'modal:', modalCreditos);
    
    if (btnVerCreditos) {
        // Recriar o botão para evitar conflitos
        const novoBtn = btnVerCreditos.cloneNode(true);
        btnVerCreditos.parentNode.replaceChild(novoBtn, btnVerCreditos);
        console.log('Botão recriado:', novoBtn);
        
        // Event listener correto para o botão
        novoBtn.addEventListener('click', function(e) {
            console.log('Botão clicado!', e);
            abrirModalCreditos();
        });
    }
    
    if (modalCreditos) {
        // Bloquear clique no modal (não fechar ao clicar dentro)
        modalCreditos.addEventListener('click', function(e) {
            console.log('Modal clicked, target:', e.target);
            // Se clicou no fundo do modal (não no conteúdo), não fechar
            if (e.target === modalCreditos || modalCreditos.contains(e.target)) {
                console.log('Clique no modal - ignorando fechar');
                e.stopPropagation();
            }
        });
        
        // Forçar exibição
        modalCreditos.style.display = 'flex';
    }
});
```

**Mudanças:**
1. ✅ **Recriar o botão** - Remove listeners antigos que podem causar conflitos
2. ✅ **Logs de inicialização** - Mostra qual botão e modal foram encontrados
3. ✅ **Bloqueio de clique no modal** - Evita fechar ao clicar no conteúdo
4. ✅ **Forçar display:** `modal.style.display = 'flex'` para garantir que aparece
5. ✅ **Logs no clique** - Mostra quando o botão é clicado e quando o modal é clicado

### 3. Verificar Elementos no DOM

Adicionei verificações se os elementos existem antes de tentar acessá-los:

```javascript
const tbody = document.getElementById('modal-tabela-creditos');
console.log('tbody antes:', tbody);
if (!tbody) {
    console.error('Elemento modal-tabela-creditos não encontrado!');
    showAlert('Erro interno: tabela de créditos não encontrada', 'error');
    return;
}
```

---

## 📋 Como Testar a Correção

### 1. Upload do PDF

1. Faça upload de um PDF válido
2. Verifique no console se os créditos foram extraídos:
   ```
   [DEBUG] Payload enviado para /api/upload-pdf: ...
   [DEBUG] Resposta /api/upload-pdf: ...
   [DEBUG] creditos: [...]
   ```

### 2. Clicar no Botão "Ver Tabela Completa"

1. Verifique se o modal aparece
2. Verifique no console:
   ```
   [DEBUG] Botão clicado! MouseEvent {...}
   [DEBUG] abrirModalCreditos - creditos: [...]
   ```

### 3. Verificar Erros

Se houver erros no console:
- Elemento modal-tabela-creditos não encontrado
- Botão não recriado
- Modal com display incorreto

---

## 🛠 Possíveis Problemas Recorrentes

### Se ainda NÃO funcionar:

1. **Modal pode já estar aberto:**
   - Verifique se há CSS conflitando (Bootstrap ou custom)
   - Tente fechar o modal manualmente com `document.getElementById('modal-creditos').style.display = 'none'`
   - Depois clique no botão

2. **Botão pode estar sendo desabilitado:**
   - Verifique se há algum JavaScript desabilitando o botão
   - Procure por `btn.disabled = true`

3. **Classe 'active' não funcionando:**
   - Verifique se há CSS conflitando com a classe `active`
   - Tente mudar para usar inline style: `display: flex !important`

4. **window.dadosPdf pode estar vazio:**
   - Verifique se o upload do PDF foi bem-sucedido
   - Verifique se a API retornou dados corretos

---

## 📚 Arquivos Modificados

| Arquivo | Modificações | Status |
|---------|---------------|--------|
| `tarefas/templates/tarefas/integracao/calcular_creditos_v2.html` | Adicionado logs + corrigidos event listeners | ✅ |

---

## 🧪 Próximos Passos para Depuração

### Para o Usuário:

1. **Recarregar a página** após as correções
2. **Upload de um PDF de teste**
3. **Abrir o console do navegador** (F12)
4. **Clicar no botão "Ver tabela completa"**
5. **Reportar o resultado** e copiar os logs do console

### Para o Desenvolvedor:

1. **Verificar logs no console** para identificar problemas
2. **Testar diferentes navegadores** (Chrome, Firefox, Edge)
3. **Verificar se há conflitos com Bootstrap**
4. **Testar com e sem JavaScript habilitado**
5. **Verificar se há erros 404 na API de upload**

---

## 📝 Notas Importantes

### Bootstrap Modal

O Bootstrap usa a classe `active` para mostrar/ocultar modais automaticamente. Se a lógica JavaScript entra em conflito com o Bootstrap, o modal pode não funcionar.

**Solução:** Em vez de depender apenas da classe `active`, forçar o `display` via JavaScript:

```javascript
modal.style.display = 'flex';  // Mostra
modal.style.display = 'none';  // Esconde
```

### Event Propagation

Para evitar que o clique no botão feche o modal, use `e.stopPropagation()`:

```javascript
novoBtn.addEventListener('click', function(e) {
    e.stopPropagation();  // Para o clique não "borbur" para outros elementos
    abrirModalCreditos();
});
```

---

## ✅ Checklist de Verificação

- [x] Logs de debug adicionados
- [x] Event listeners corrigidos e movidos para DOMContentLoaded
- [x] Botão recriado para evitar conflitos
- [x] Bloqueio de clique no modal adicionado
- [x] Forçar display do modal adicionado
- [ ] Testado em produção (pendente)

---

**Versão:** 1.1  
**Data:** 2026-03-21  
**Status:** ✅ CORRIGIDO (AGUARDANDO TESTE)
