#!/bin/bash
# Script de sincronização para projeto SAACB
# Copia os arquivos atualizados do workspace-dev para o CASAOS

WORKSPACE="/data/.openclaw/workspace-dev/projeto-saacb"
CASAOSS="/DATA/AppData/fitt/projeto-saacb"

echo "=========================================="
echo "Sincronizando SAACB para CASAOS"
echo "=========================================="

# Verificar se diretórios existem
if [ ! -d "$WORKSPACE" ]; then
    echo "ERRO: Diretório workspace não encontrado: $WORKSPACE"
    exit 1
fi

if [ ! -d "$CASAOSS" ]; then
    echo "ERRO: Diretório CASAOS não encontrado: $CASAOSS"
    exit 1
fi

# Copiar settings.py
echo "[1/6] Copiando settings.py..."
sudo cp "$WORKSPACE/projeto_saacb/settings.py" "$CASAOSS/projeto_saacb/settings.py"

# Copiar urls.py
echo "[2/6] Copiando urls.py..."
sudo cp "$WORKSPACE/projeto_saacb/urls.py" "$CASAOSS/projeto_saacb/urls.py"

# Copiar views.py (tarefas e dashboards)
echo "[3/6] Copiando views..."
sudo cp "$WORKSPACE/tarefas/views.py" "$CASAOSS/tarefas/views.py"
sudo cp "$WORKSPACE/dashboards/views.py" "$CASAOSS/dashboards/views.py"

# Copiar templates
echo "[4/6] Sincronizando templates..."
sudo mkdir -p "$CASAOSS/templates"
sudo rm -rf "$CASAOSS/templates"/*
sudo cp -r "$WORKSPACE/templates/"* "$CASAOSS/templates/"

# Copiar arquivos estáticos
echo "[5/6] Copiando arquivos estáticos..."
sudo mkdir -p "$CASAOSS/static"
sudo cp -r "$WORKSPACE/static/"* "$CASAOSS/static/"

# Copiar docker-compose.yml
echo "[6/6] Copiando docker-compose.yml..."
sudo cp "$WORKSPACE/docker-compose.yml" "$CASAOSS/docker-compose.yml"

echo ""
echo "=========================================="
echo "Sincronização concluída!"
echo "=========================================="
echo ""
echo "Para aplicar as mudanças:"
echo "  cd /DATA/AppData/fitt/projeto-saacb"
echo "  docker-compose down"
echo "  docker-compose up -d"
echo ""
