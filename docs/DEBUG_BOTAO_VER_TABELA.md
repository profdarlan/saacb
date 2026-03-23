# 🐛 DEBUG: Botão "Ver Tabela Completa" não Funcionando

**Data:** 2026-03-21  
**Status:** ⏳ Em investigação

---

## 🎯 Problema

O botão `👁️ Ver tabela completa dos créditos extraídos` não está abrindo o modal corretamente.

---

## 🔍 Possíveis Causas

### 1. Modal não está sendo exibido

**Verificar:**
```javascript
// Console do navegador
document.getElementById('modal-creditos')
// Deve retornar o elemento do modal
```

### 2. Event listener não foi configurado

**Verificar:**
```javascript
// No console
window.dadosPdf
// Deve ter { creditos: [...], beneficiario: {...} }
```

### 3. Atributo `class="active"` não está sendo definido

**Verificar:**
```html
<!-- Verifique se o modal tem a classe "active" quando aberto -->
<div id="modal-creditos" class="modal active">  <!-- ← "active" deve estar aqui -->
```

---

## 🛠 Como Debugar

### 1. Adicionar logs no JavaScript

Adicione este código no início da tag `<script>`:

```javascript
// DEBUG LOG
const DEBUG = true;

function debugLog(msg, data = null) {
    if (!DEBUG) return;
    console.log(`[DEBUG] ${msg}`, data);
}

// Log quando dadosPdf é atualizado
const originalDadosPdf = window.dadosPdf;
Object.defineProperty(window, 'dadosPdf', {
    get: () => window._dadosPdf,
    set: (val) => {
        window._dadosPdf = val;
        debugLog('dadosPdf atualizado:', val);
    }
});
```

### 2. Verificar se o modal existe

Adicione no início da tag `<script>`:

```javascript
// Verificar elementos ao carregar
document.addEventListener('DOMContentLoaded', () => {
    debugLog('Elementos encontrados:', {
        modalCreditos: !!document.getElementById('modal-creditos'),
        btnVerCreditos: !!document.getElementById('btn-ver-creditos'),
        dadosPdf: window.dadosPdf
    });
});
```

### 3. Testar manualmente

No console do navegador:

```javascript
// Testar manualmente abrir o modal
abrirModalCreditos();

// Testar se há dados
console.log('creditos:', window.dadosPdf?.creditos);
```

---

## ✅ Solução Proposta

### Opção 1: Atributo `onclick` no botão

```html
<!-- No template, trocar -->
<button type="button" class="btn btn-outline-info btn-sm" id="btn-ver-creditos">
    👁️ Ver tabela completa dos créditos extraídos
</button>

<!-- Por -->
<button type="button" class="btn btn-outline-info btn-sm" id="btn-ver-creditos" onclick="abrirModalCreditos(); return false;">
    👁️ Ver tabela completa dos créditos extraídos
</button>
```

### Opção 2: Mover o event listener para antes do modal

```javascript
// Mover o event listener para antes de tentar fechar o modal
document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('btn-ver-creditos');
    const modal = document.getElementById('modal-creditos');
    
    if (btn && modal) {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            abrirModalCreditos();
        });
    }
});
```

### Opção 3: Verificar se há conflito de ID

Verifique se não há outro elemento com `id="modal-creditos"` ou `id="btn-ver-creditos"` na página.

---

## 📋 Checklist para Resolução

- [ ] Verificar se o elemento modal existe no DOM
- [ ] Verificar se `window.dadosPdf` tem dados após upload do PDF
- [ ] Verificar se há conflitos de IDs
- [ ] Testar o botão no console do navegador
- [ ] Verificar se há erros no console do navegador
- [ ] Aplicar solução (Opção 1, 2 ou 3)
- [ ] Testar após a aplicação da solução

---

## 📝 Observações Importantes

1. **O modal só abre se `window.dadosPdf.creditos` tiver dados**
   
2. **O upload do PDF popula `window.dadosPdf` automaticamente**

3. **Se o PDF não foi processado ainda, o botão deve mostrar alert**

4. **Verifique a ordem dos scripts:** JavaScript que manipula o DOM deve estar carregado antes do código do modal

---

**Versão:** 1.0  
**Data:** 2026-03-21  
**Status:** ⏳ Em investigação
