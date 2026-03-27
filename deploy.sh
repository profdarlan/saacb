#!/bin/bash

# Deploy SAACB - Fluxo Git-based
# Produção: Atualiza arquivos de produção, commit, push, usuário autoriza
# Desenvolvimento: Commit, push automático

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warning() { echo -e "${YELLOW}[AVISO]${NC} $1"; }
error() { echo -e "${RED}[ERRO]${NC} $1"; exit 1; }

# Configurações
REPO_DEV="/data/.openclaw/workspace-dev/projeto-saacb"
REPO_PROD="/data/.openclaw/workspace-dev/saacb-django-prod"
GITHUB_USER="profdarlan"

# Detectar ambiente
if [ -z "$1" ]; then
    error "Uso: $0 [dev|prod]"
fi

AMBIENTE=$1
CURRENT_DIR=$(basename $(pwd))

# Validação de ambiente
if [ "$AMBIENTE" = "dev" ]; then
    if [ "$CURRENT_DIR" != "projeto-saacb" ]; then
        error "Você deve estar em 'projeto-saacb' para deploy de desenvolvimento"
    fi
    log "Ambiente: DESENVOLVIMENTO"
    CONTAINER="saacb-django-dev"
    CASAOS_DIR="/DATA/AppData/fitt/projeto-saacb"
    SETTINGS_FILE="settings_dev.py"
    COMPOSE_FILE="docker-compose.yml"
    PORTA="30010"
    GIT_REPO="saacb.git"
    REPO_LOCAL="$REPO_DEV"

elif [ "$AMBIENTE" = "prod" ]; then
    if [ "$CURRENT_DIR" != "saacb-django-prod" ]; then
        error "Você deve estar em 'saacb-django-prod' para deploy de produção"
    fi
    log "Ambiente: PRODUÇÃO"
    CONTAINER="saacb-django-prod"
    CASAOS_DIR="/DATA/AppData/saacb-django-prod"
    SETTINGS_FILE="settings.py"
    COMPOSE_FILE="docker-compose.yml"
    PORTA="8000"
    GIT_REPO="saacb-django-prod.git"
    REPO_LOCAL="$REPO_PROD"
else
    error "Ambiente inválido: $1 (use: dev ou prod)"
fi

# Verificar se está em um repositório git
if [ ! -d ".git" ]; then
    error "Diretório atual não é um repositório git"
fi

# ===================================================================
# FUNÇÕES DE CONFIGURAÇÃO
# ===================================================================

configurar_producao() {
    log "Configurando ambiente de PRODUÇÃO..."

    # Atualizar settings.py para produção
    if [ -f "projeto_saacb/settings.py" ]; then
        log "Atualizando settings.py..."

        # DEBUG deve ser False
        sed -i 's/^DEBUG = .*/DEBUG = False/' projeto_saacb/settings.py

        # ALLOWED_HOSTS para produção
        sed -i 's/ALLOWED_HOSTS = \[.*/ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.1.51", "saacb.lakeserver.online"]/' projeto_saacb/settings.py

        # Banco de dados de produção
        sed -i 's|data/db_dev.sqlite3|data/db.sqlite3|g' projeto_saacb/settings.py

        # Desabilitar e-mail de console em produção
        sed -i 's/EMAIL_BACKEND.*/EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"/' projeto_saacb/settings.py

        success "settings.py configurado para produção"
    fi

    # Atualizar docker-compose.yml se necessário
    if [ -f "docker-compose.yml" ]; then
        # Verificar se porta está correta
        if grep -q '30010:8000' docker-compose.yml; then
            sed -i 's/30010:8000/8000:8000/' docker-compose.yml
            success "Porta docker-compose.yml corrigida para 8000"
        fi
    fi

    log ""
    warning "Verifique as configurações de produção:"
    echo "  - DEBUG: False"
    echo "  - Porta: 8000"
    echo "  - URL: https://saacb.lakeserver.online"
    echo "  - Banco: data/db.sqlite3"
    echo ""
}

configurar_desenvolvimento() {
    log "Configurando ambiente de DESENVOLVIMENTO..."

    # Criar settings_dev.py se não existir
    if [ ! -f "projeto_saacb/settings_dev.py" ]; then
        warning "settings_dev.py não encontrado, usando settings.py"
        warning "Considere criar um settings_dev.py separado"
    else
        # DEBUG deve ser True
        sed -i 's/^DEBUG = .*/DEBUG = True/' projeto_saacb/settings_dev.py

        # ALLOWED_HOSTS para desenvolvimento
        sed -i 's/ALLOWED_HOSTS = \[.*/ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.1.51", "192.168.1.51:30010"]/' projeto_saacb/settings_dev.py

        # Banco de dados de desenvolvimento
        sed -i 's|data/db.sqlite3|data/db_dev.sqlite3|g' projeto_saacb/settings_dev.py

        # Email em modo console
        sed -i 's/EMAIL_BACKEND.*/EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"/' projeto_saacb/settings_dev.py

        success "settings_dev.py configurado para desenvolvimento"
    fi

    # Atualizar docker-compose.yml se necessário
    if [ -f "docker-compose.yml" ]; then
        # Verificar se porta está correta
        if grep -q '8000:8000' docker-compose.yml; then
            sed -i 's/8000:8000/30010:8000/' docker-compose.yml
            success "Porta docker-compose.yml corrigida para 30010"
        fi
    fi

    log ""
    log "Configurações de desenvolvimento aplicadas:"
    echo "  - DEBUG: True"
    echo "  - Porta: 30010"
    echo "  - URL: http://192.168.1.51:30010"
    echo "  - Banco: data/db_dev.sqlite3"
    echo ""
}

# ===================================================================
# DESENVOLVIMENTO
# ===================================================================

if [ "$AMBIENTE" = "dev" ]; then
    log "=== DEPLOY DESENVOLVIMENTO ==="
    echo ""

    # Configurar ambiente
    configurar_desenvolvimento

    # Verificar mudanças
    log "Verificando mudanças no repositório..."
    if git diff-index --quiet HEAD --; then
        warning "Nenhuma mudança encontrada. Nada para commitar."
        log "Para atualizar o CasaOS, execute:"
        echo "  ./pull.sh dev"
        exit 0
    fi

    # Mostrar mudanças
    log "Mudanças encontradas:"
    git status --short
    echo ""

    # Commit
    log "Fazendo commit das mudanças..."
    COMMIT_MSG="deploy-dev: $(date '+%Y-%m-%d %H:%M:%S') - atualizações de desenvolvimento"
    git add -A
    git commit -m "$COMMIT_MSG"
    success "Commit criado: $COMMIT_MSG"

    # Push automático (sem confirmação)
    log "Fazendo push para GitHub..."
    git push origin main
    success "Push realizado para origin/main"

    log ""
    echo -e "${GREEN}═════════════════════════════════════${NC}"
    echo -e "${GREEN}  DEPLOY DESENVOLVIMENTO CONCLUÍDO${NC}"
    echo -e "${GREEN}═════════════════════════════════════${NC}"
    echo ""
    log "Próximo passo: Atualizar no servidor CasaOS"
    echo "  ./pull.sh dev"
    echo ""
    echo "Ou acessar via interface web do CasaOS e fazer pull no container."

fi

# ===================================================================
# PRODUÇÃO
# ===================================================================

if [ "$AMBIENTE" = "prod" ]; then
    log "=== DEPLOY PRODUÇÃO ==="
    echo ""

    # Confirmar deploy de produção
    echo -e "${RED}═════════════════════════════════════${NC}"
    echo -e "${RED}  DEPLOY PARA PRODUÇÃO SAACB${NC}"
    echo -e "${RED}═════════════════════════════════════${NC}"
    echo ""
    echo "Repositório: $GIT_REPO"
    echo "Container: $CONTAINER"
    echo "Porta: $PORTA"
    echo "URL: https://saacb.lakeserver.online"
    echo ""
    echo -e "${YELLOW}AVISO: Isso atualizará a versão em produção!${NC}"
    read -p "Confirmar deploy para produção? (sim/não): " CONFIRMACAO

    if [ "$CONFIRMACAO" != "sim" ]; then
        log "Deploy cancelado pelo usuário"
        exit 0
    fi

    # Configurar ambiente de produção
    configurar_producao

    # Verificar mudanças
    log "Verificando mudanças no repositório..."
    if git diff-index --quiet HEAD --; then
        warning "Nenhuma mudança encontrada."
        log "Para atualizar o CasaOS, execute:"
        echo "  ./pull.sh prod"
        exit 0
    fi

    # Mostrar mudanças
    log "Mudanças encontradas:"
    git status --short
    echo ""

    # Commit (requer confirmação do usuário)
    log "Fazendo commit das mudanças..."
    read -p "Mensagem do commit (ou Enter para usar padrão): " MSG_USER

    if [ -z "$MSG_USER" ]; then
        COMMIT_MSG="deploy-prod: $(date '+%Y-%m-%d %H:%M:%S') - atualizações de produção"
    else
        COMMIT_MSG="deploy-prod: $MSG_USER"
    fi

    git add -A
    git commit -m "$COMMIT_MSG"
    success "Commit criado: $COMMIT_MSG"

    # Push (requer confirmação do usuário)
    echo ""
    read -p "Fazer push para GitHub agora? (sim/não): " PUSH_CONFIRMACAO

    if [ "$PUSH_CONFIRMACAO" != "sim" ]; then
        log "Push não realizado. Você pode fazer depois com: git push"
        exit 0
    fi

    log "Fazendo push para GitHub..."
    git push origin main
    success "Push realizado para origin/main"

    log ""
    echo -e "${GREEN}═════════════════════════════════════${NC}"
    echo -e "${GREEN}  DEPLOY PRODUÇÃO CONCLUÍDO (GIT)${NC}"
    echo -e "${GREEN}═════════════════════════════════════${NC}"
    echo ""
    log "Próximo passo: Atualizar no servidor CasaOS"
    echo "  ./pull.sh prod"
    echo ""
    echo "O servidor CasaOS já está configurado com ambiente de produção."
fi
