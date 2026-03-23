# 🎨 SAACB Design System

Design System baseado na identidade visual INSS, com componentes reutilizáveis e consistentes.

## 📋 Índice

1. [Instalação](#instalação)
2. [Variáveis CSS](#variáveis-css)
3. [Componentes](#componentes)
4. [Exemplos de Uso](#exemplos-de-uso)

---

## 🔧 Instalação

### 1. Adicionar o CSS do Design System

No `base.html`, adicione após o style.css existente:

```html
<!-- Design System CSS -->
<link href="{% static 'css/design-system.css' %}" rel="stylesheet">
```

### 2. Estrutura de Templates

```
templates/
└── design-system/
    ├── button.html      # Componente de botão
    ├── card.html        # Componente de card
    ├── badge.html       # Componente de badge
    ├── stat-card.html   # Componente de estatística
    └── empty-state.html # Estado vazio
```

---

## 🎨 Variáveis CSS

### Cores

```css
/* Primárias (Tema INSS) */
--ds-primary: #005696;
--ds-primary-hover: #003d6b;
--ds-accent: #ffcc00;

/* Funcionais */
--ds-success: #28a745;
--ds-warning: #ffc107;
--ds-danger: #dc3545;
--ds-info: #17a2b8;

/* Neutros */
--ds-gray-50: #f8f9fa;
--ds-gray-900: #212529;
--ds-white: #ffffff;
```

### Tipografia

```css
--ds-font-size-sm: 0.875rem;
--ds-font-size-base: 1rem;
--ds-font-size-lg: 1.125rem;
--ds-font-size-xl: 1.25rem;
--ds-font-size-2xl: 1.5rem;
--ds-font-weight-medium: 500;
--ds-font-weight-bold: 700;
```

### Espaçamentos

```css
--ds-spacing-xs: 0.25rem;
--ds-spacing-sm: 0.5rem;
--ds-spacing-md: 1rem;
--ds-spacing-lg: 1.5rem;
--ds-spacing-xl: 2rem;
```

### Border Radius

```css
--ds-radius-md: 0.375rem;
--ds-radius-lg: 0.5rem;
--ds-radius-xl: 0.75rem;
--ds-radius-full: 9999px;
```

---

## 🧩 Componentes

### 1. Botões (Button)

#### Uso Básico
```django
{% include "design-system/button.html" with text="Salvar" variant="primary" %}
```

#### Com Ícone
```django
{% include "design-system/button.html" with text="Salvar" variant="primary" icon="check" %}
```

#### Como Link
```django
{% include "design-system/button.html" with text="Editar" variant="outline" href="/editar/" icon="pencil" %}
```

#### Opções
- `text` - Texto do botão
- `variant` - primary, success, danger, outline
- `icon` - Ícone Bootstrap Icons (sem o prefixo bi-)
- `href` - Se definido, cria um link em vez de button
- `type` - button, submit (padrão: button)
- `size` - sm, md, lg (padrão: md)
- `class` - Classes CSS adicionais
- `disabled` - Se verdadeiro, desabilita o botão

#### Exemplos
```django
<!-- Botão Principal -->
{% include "design-system/button.html" with text="Criar Tarefa" variant="primary" icon="plus-circle" %}

<!-- Botão de Sucesso -->
{% include "design-system/button.html" with text="Confirmar" variant="success" icon="check-circle" %}

<!-- Botão de Perigo -->
{% include "design-system/button.html" with text="Excluir" variant="danger" icon="trash" %}

<!-- Botão Outline -->
{% include "design-system/button.html" with text="Cancelar" variant="outline" icon="x" %}
```

---

### 2. Cards (Card)

#### Uso Básico
```django
{% include "design-system/card.html" with title="Meus Dados" icon="person" %}
    <p>Conteúdo do card aqui...</p>
{% endinclude %}
```

#### Sem Header
```django
{% include "design-system/card.html" with no_header=true %}
    <p>Card sem título</p>
{% endinclude %}
```

#### Opções
- `title` - Título do card (exibe no header)
- `icon` - Ícone do Bootstrap Icons
- `header_class` - Classes CSS adicionais para o header
- `body_class` - Classes CSS adicionais para o corpo
- `no_header` - Se verdadeiro, não exibe o header
- `no_footer` - Se verdadeiro, não exibe o footer

#### Exemplos
```django
<!-- Card Simples -->
{% include "design-system/card.html" with title="Informações" icon="info-circle" %}
    <p>Detalhes importantes...</p>
{% endinclude %}

<!-- Card com Conteúdo Customizado -->
{% include "design-system/card.html" with title="Gráfico de Vendas" icon="bar-chart" %}
    <canvas id="vendasChart"></canvas>
{% endinclude %}
```

---

### 3. Badges (Badge)

#### Uso Básico
```django
{% include "design-system/badge.html" with text="Pendente" variant="warning" %}
```

#### Com Ícone
```django
{% include "design-system/badge.html" with text="Concluído" variant="success" icon="check-circle" %}
```

#### Opções
- `text` - Texto do badge
- `variant` - primary, success, warning, danger, info
- `icon` - Ícone Bootstrap Icons
- `class` - Classes CSS adicionais

#### Exemplos
```django
<!-- Status Pendente -->
{% include "design-system/badge.html" with text="Pendente" variant="warning" %}

<!-- Status Concluído -->
{% include "design-system/badge.html" with text="Concluído" variant="success" icon="check" %}

<!-- Status de Erro -->
{% include "design-system/badge.html" with text="Erro" variant="danger" icon="exclamation-triangle" %}

<!-- Informação -->
{% include "design-system/badge.html" with text="Novo" variant="info" icon="star" %}
```

---

### 4. Stat Cards (Stat Card)

#### Uso Básico
```django
{% include "design-system/stat-card.html" with icon="clock" value="10" label="Pendentes" variant="warning" %}
```

#### Opções
- `icon` - Ícone Bootstrap Icons
- `value` - Valor numérico
- `label` - Texto descritivo
- `variant` - primary, success, warning, danger, info
- `class` - Classes CSS adicionais

#### Exemplos
```django
<!-- Pendentes -->
{% include "design-system/stat-card.html" with icon="clock-history" value="15" label="Pendentes" variant="warning" %}

<!-- Concluídas -->
{% include "design-system/stat-card.html" with icon="check-circle" value="45" label="Concluídas" variant="success" %}

<!-- Total -->
{% include "design-system/stat-card.html" with icon="list-check" value="60" label="Total" variant="primary" %}
```

---

### 5. Empty State (Estado Vazio)

#### Uso Básico
```django
{% include "design-system/empty-state.html" with icon="clipboard-x" title="Sem Tarefas" description="Não há tarefas cadastradas." action_url="/criar/" action_text="Criar Nova" %}
```

#### Sem Ação
```django
{% include "design-system/empty-state.html" with icon="search" title="Sem Resultados" description="Sua busca não retornou resultados." %}
```

#### Opções
- `icon` - Ícone Bootstrap Icons
- `title` - Título do estado vazio
- `description` - Texto descritivo
- `action_url` - URL do botão de ação
- `action_text` - Texto do botão de ação
- `action_icon` - Ícone do botão de ação

#### Exemplos
```django
<!-- Lista Vazia -->
{% include "design-system/empty-state.html" with icon="clipboard-x" title="Nenhuma Tarefa" description="Você não tem tarefas atribuídas." action_url="/tarefas/criar/" action_text="Criar Nova Tarefa" action_icon="plus-circle" %}

<!-- Busca Sem Resultados -->
{% include "design-system/empty-state.html" with icon="search" title="Sem Resultados" description="Nenhuma tarefa corresponde à sua busca." %}

<!-- Filtros Vazios -->
{% include "design-system/empty-state.html" with icon="funnel" title="Nenhum Resultado" description="Tente ajustar os filtros de busca." %}
```

---

## 📐 Layouts Pré-definidos

### Grid de Estatísticas
```django
<div class="row">
    <div class="col-12 col-sm-6 col-lg-3 mb-3">
        {% include "design-system/stat-card.html" with icon="clock-history" value="10" label="Pendentes" variant="warning" %}
    </div>
    <div class="col-12 col-sm-6 col-lg-3 mb-3">
        {% include "design-system/stat-card.html" with icon="check-circle" value="25" label="Concluídas" variant="success" %}
    </div>
    <div class="col-12 col-sm-6 col-lg-3 mb-3">
        {% include "design-system/stat-card.html" with icon="calendar-week" value="8" label="Esta Semana" variant="info" %}
    </div>
    <div class="col-12 col-sm-6 col-lg-3 mb-3">
        {% include "design-system/stat-card.html" with icon="exclamation-triangle" value="2" label="Faltam" variant="danger" %}
    </div>
</div>
```

### Barra de Ferramentas
```django
<div class="ds-search-toolbar">
    <div class="row align-items-center">
        <div class="col-12 col-lg-6">
            <form method="get">
                <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-search"></i></span>
                    <input type="search" name="q" class="ds-input" placeholder="Buscar...">
                    <button type="submit" class="ds-btn ds-btn-primary">Buscar</button>
                </div>
            </form>
        </div>
        <div class="col-12 col-lg-6">
            <div class="d-flex justify-content-end gap-2">
                {% include "design-system/button.html" with text="Novo" variant="primary" icon="plus" href="/criar/" %}
                {% include "design-system/button.html" with text="Exportar" variant="outline" icon="download" href="/exportar/" %}
            </div>
        </div>
    </div>
</div>
```

---

## 🎯 Boas Práticas

### 1. Consistência
- Sempre use os componentes do Design System
- Mantenha os textos curtos e diretos
- Use ícones que complementam o texto

### 2. Acessibilidade
- Sempre forneça texto descritivo para ícones
- Use variantes de cores de forma consistente
- Garanta contraste adequado

### 3. Responsividade
- Use as classes de grid do Bootstrap (col-* )
- Teste em diferentes tamanhos de tela
- Use espaçamentos flexíveis

---

## 🚀 Roadmap

- [ ] Componentes de Formulário (Input, Select, Checkbox)
- [ ] Componentes de Tabela (com ordenação e filtros)
- [ ] Componentes de Modal
- [ ] Componentes de Toast/Notificação
- [ ] Componentes de Dropdown
- [ ] Componentes de Tabs
- [ ] Componentes de Accordion
- [ ] Documentação Storybook

---

**Versão:** 1.0.0
**Data:** Março 2026
**Tema:** Identidade Visual INSS
