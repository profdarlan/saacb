# 📚 Índice da Documentação SAACB

**Versão:** 1.1  
**Data:** 2026-03-21  
**Status:** ✅ Atualizado

---

## 📖 Documentação Principal

| Arquivo | Descrição | Última Atualização |
|---------|-----------|-------------------|
| [README.md](../README.md) | README minimal (aponta para docs/) | 2026-03-21 |
| [README.md](README.md) | Documentação completa do sistema | 2026-03-19 |
| [ANALISE_COMPLETA_20260321.md](ANALISE_COMPLETA_20260321.md) | Análise completa para deploys | 2026-03-21 |
| [STATUS.md](STATUS.md) | Status atual do sistema | 2025-03-19 |

---

## 🧠 Documentação para IA

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| [MAPEAMENTO_SISTEMA_IA.md](MAPEAMENTO_SISTEMA_IA.md) | Mapeamento completo do sistema | Diagnóstico de bugs e entendimento de arquitetura |
| [RESUMO_IA.md](RESUMO_IA.md) | Resumo rápido para consulta | Referência rápida durante debug |

---

## 🔧 Docker e Deploy

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| [DOCKER.md](DOCKER.md) | Guia completo Docker | Deploy com Docker |
| [RESUMO_FINAL_DOCKER.md](RESUMO_FINAL_DOCKER.md) | Resumo do projeto Docker | Overview rápido do Docker |
| [CORRECOES_DOCKER.md](CORRECOES_DOCKER.md) | Histórico correções Docker | Troubleshooting Docker |
| [DOCKERFILE_CORRIGIDO.md](DOCKERFILE_CORRIGIDO.md) | Correções do Dockerfile | Referência Dockerfile |
| [DOCKER_NAO_ACESSIVEL.md](DOCKER_NAO_ACESSIVEL.md) | Problema Docker não acessível | Troubleshooting |
| [COMANDOS_COPIAR_DOCKER.md](COMANDOS_COPIAR_DOCKER.md) | Comandos prontos para copiar | Deploy rápido |
| [GUIA_COPIAR_DOCKER.md](GUIA_COPIAR_DOCKER.md) | Guia completo 3 métodos | Copiar arquivos para Docker |

---

## 🐛 Correções e Bugs

| Arquivo | Descrição | Data |
|---------|-----------|------|
| [CONSOLIDADO_CORRECOES_20260321.md](CONSOLIDADO_CORRECOES_20260321.md) | Consolidado das 2 correções de hoje | 2026-03-21 |
| [CORRECAO_REDIRECT_PARAMETRO_20260321.md](CORRECAO_REDIRECT_PARAMETRO_20260321.md) | Correção: Parâmetro errado no redirect() | 2026-03-21 |
| [CORRECAO_NOREVERSMATCH_20260321.md](CORRECAO_NOREVERSMATCH_20260321.md) | Correção: Nome da URL em views_integracao.py | 2026-03-21 |
| [CORRECAO_FINAL_TEMPLATE.md](CORRECAO_FINAL_TEMPLATE.md) | Correção template path | 2025-03-20 |
| [CORRECAO_TEMPLATE_UPLOAD_PDF.md](CORRECAO_TEMPLATE_UPLOAD_PDF.md) | Correção template: upload + API 8002 | 2025-03-20 |
| [CORRECAO_URL_TAREFA_LIST.md](CORRECAO_URL_TAREFA_LIST.md) | Correção URL namespace | 2025-03-20 |
| [RESUMO_CORRECOES.md](RESUMO_CORRECOES.md) | Histórico de correções | 2025-03-20 |
| [ARQUIVOS_CORRIGIDOS.md](ARQUIVOS_CORRIGIDOS.md) | Lista de arquivos corrigidos | 2025-03-20 |

---

## 🔄 Migrations

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| [GUIA_MIGRATIONS_DOCKER.md](GUIA_MIGRATIONS_DOCKER.md) | Guia de aplicações de migrations | Deploy migrations no Docker |
| [FIX_MIGRATIONS_DOCKER.md](FIX_MIGRATIONS_DOCKER.md) | Guia rápido correção migrations | Corrigir erros de migration |

---

## ⚡ Funcionalidades

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| [GUIA_CALCULOS.md](GUIA_CALCULOS.md) | Guia funcionalidade de cálculos | Usar cálculos de créditos |
| [RESUMO_IMPLEMENTACAO.md](RESUMO_IMPLEMENTACAO.md) | Resumo completo da implementação | Visão geral da implementação |
| [RESUMO_INTEGRACAO.md](RESUMO_INTEGRACAO.md) | Resumo da integração | Integração SAACB ↔ Planilha Cálculos |
| [RESUMO_MENU_CALCULOS.md](RESUMO_MENU_CALCULOS.md) | Resumo menu cálculos | Navegação da interface |

---

## 🎨 Design System

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) | Documentação do Design System | Desenvolvimento frontend |

---

## 🎯 Botões e Interface

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| [BOTAO_CALCULAR_DETALHES.md](BOTAO_CALCULAR_DETALHES.md) | Botão nos detalhes | Implementação botão calcular |

---

## 🔍 Como Usar Esta Documentação

### Para Diagnóstico de Bugs

1. Comece com **[RESUMO_IA.md](RESUMO_IA.md)** para referência rápida
2. Se necessário, consulte **[MAPEAMENTO_SISTEMA_IA.md](MAPEAMENTO_SISTEMA_IA.md)** para entendimento profundo
3. Verifique **[Erros Conhecidos em RESUMO_IA.md](RESUMO_IA.md#️-erros-conhecidos)**
4. Consulte arquivos de **[Correções](#️-correções-e-bugs)** se o erro já foi documentado

### Para Deploy

1. **[ANALISE_COMPLETA_20260321.md](ANALISE_COMPLETA_20260321.md)** - Análise completa pré-deploy
2. **[DOCKER.md](DOCKER.md)** - Guia completo
3. **[COMANDOS_COPIAR_DOCKER.md](COMANDOS_COPIAR_DOCKER.md)** - Comandos prontos
4. **[GUIA_MIGRATIONS_DOCKER.md](GUIA_MIGRATIONS_DOCKER.md)** - Aplicar migrations

### Para Desenvolvimento

1. **[README.md](README.md)** - Documentação principal
2. **[DESIGN-SYSTEM.md](DESIGN-SYSTEM.md)** - Design System
3. **[GUIA_CALCULOS.md](GUIA_CALCULOS.md)** - Funcionalidades de cálculo

---

## 📝 Convenções de Nomenclatura

### Prefixos de Arquivos

| Prefixo | Significado | Exemplo |
|----------|-------------|----------|
| `README.md` | Documentação principal | `README.md` |
| `RESUMO_*.md` | Resumos de tópicos | `RESUMO_CORRECOES.md` |
| `CORRECAO_*.md` | Correções específicas | `CORRECAO_NOREVERSMATCH_20260321.md` |
| `GUIA_*.md` | Guias práticos | `GUIA_CALCULOS.md` |
| `FIX_*.md` | Correções rápidas | `FIX_MIGRATIONS_DOCKER.md` |

### Formato de Data em Arquivos de Correção

`CORRECAO_NOMEBUG_YYYYMMDD.md`

- `NOMEBUG`: Nome do erro em maiúsculas (ex: NOREVERSMATCH)
- `YYYYMMDD`: Ano, mês, dia da correção

---

## 🔄 Atualizações Recentes

### 2026-03-21
- ✅ Criado **[ANALISE_COMPLETA_20260321.md](ANALISE_COMPLETA_20260321.md)** - Análise completa do projeto
- ✅ Criado **[CORRECAO_NOREVERSMATCH_20260321.md](CORRECAO_NOREVERSMATCH_20260321.md)** - Correção NoReverseMatch
- ✅ Movidos todos os arquivos `.md` para `docs/`
- ✅ Criado **[MAPEAMENTO_SISTEMA_IA.md](MAPEAMENTO_SISTEMA_IA.md)** - 38KB de documentação
- ✅ Criado **[RESUMO_IA.md](RESUMO_IA.md)** - 8KB de resumo
- ✅ Criado este **[INDEX.md](INDEX.md)** - Índice da documentação
- ✅ Aplicadas migrations 0015 e 0016
- ✅ Verificado banco de dados (86 tarefas)

### 2025-03-20
- ✅ Organização completa da documentação
- ✅ Correções de template e URLs

---

## 📊 Estatísticas da Documentação

| Categoria | Quantidade |
|-----------|------------|
| **Documentação Principal** | 4 arquivos |
| **Documentação para IA** | 2 arquivos |
| **Docker e Deploy** | 7 arquivos |
| **Correções e Bugs** | 6 arquivos |
| **Migrations** | 2 arquivos |
| **Funcionalidades** | 4 arquivos |
| **Design System** | 1 arquivo |
| **Botões e Interface** | 1 arquivo |
| **TOTAL** | **27 arquivos** |

---

**Versão:** 1.1  
**Data:** 2026-03-21  
**Status:** ✅ Organizado e atualizado