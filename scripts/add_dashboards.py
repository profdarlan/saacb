#!/usr/bin/env python3
# Script para adicionar dashboards ao INSTALLED_APPS

settings_file = 'projeto_saacb/settings.py'

# Ler o arquivo
with open(settings_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar dashboards após tarefas.apps.TarefasConfig
old_text = "    'tarefas.apps.TarefasConfig',  # importante: não apenas 'tarefas'\n]"
new_text = "    'tarefas.apps.TarefasConfig',  # importante: não apenas 'tarefas'\n    'dashboards.apps.DashboardsConfig',  # Dashboard SAMC\n]"

content = content.replace(old_text, new_text)

# Salvar
with open(settings_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ App dashboards adicionado ao INSTALLED_APPS")
print("   - Após 'tarefas.apps.TarefasConfig'")
print("   - Nome: DashboardsConfig")
