#!/bin/bash

# Pull no CasaOS para atualizar ambiente
# Uso: ./pull.sh [dev|prod]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
error() { echo -e "${RED}[ERRO]${NC} $1"; exit 1; }

# Configurações
CASASOS_USER="fitt@192.168.1.51"
CASASOS_DEV_DIR="/DATA/AppData/fitt/projeto-saacb"
CASASOS_PROD_DIR="/DATA/AppData/saacb-django-prod"

# Verificar argumentos
if [ -z "$1" ]; then
    error "Uso: $0 [dev|prod]"
fi

AMBIENTE=$1

if [ "$AMBIENTE" = "dev" ]; then
    log "=== PULL DESENVOLVIMENTO NO CASAOS ==="
    echo ""
    log "Diretório: $CASASOS_DEV_DIR"
    log "Container: saacb-django-dev"
    log "Porta: 30010"
    echo ""

    log "Fazendo git pull..."
    ssh "$CASASOS_USER" "cd $CASASOS_DEV_DIR && git pull"

    log "Reiniciando container..."
    ssh "$CASASOS_USER" "docker restart saacb-django-dev"

    success "Pull e restart concluídos!"
    echo ""
    echo "Acesse: http://192.168.1.51:30010"

elif [ "$AMBIENTE" = "prod" ]; then
    log "=== PULL PRODUÇÃO NO CASAOS ==="
    echo ""

    # Confirmação
    echo -e "${RED}═════════════════════════════════════${NC}"
    echo -e "${RED}  PULL PRODUÇÃO NO CASAOS${NC}"
    echo -e "${RED}═════════════════════════════════════${NC}"
    echo ""
    log "Diretório: $CASASOS_PROD_DIR"
    log "Container: saacb-django-prod"
    log "Porta: 8000"
    log "URL: https://saacb.lakeserver.online"
    echo ""
    read -p "Confirmar pull de produção? (sim/não): " CONFIRMACAO

    if [ "$CONFIRMACAO" != "sim" ]; then
        log "Pull cancelado"
        exit 0
    fi

    log "Fazendo git pull..."
    ssh "$CASASOS_USER" "cd $CASASOS_PROD_DIR && git pull"

    log "Reiniciando container..."
    ssh "$CASASOS_USER" "docker restart saacb-django-prod"

    success "Pull e restart concluídos!"
    echo ""
    echo "Acesse: https://saacb.lakeserver.online"

else
    error "Ambiente inválido: $1 (use: dev ou prod)"
fi
