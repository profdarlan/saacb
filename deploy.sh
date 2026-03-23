#!/bin/bash
# Script de Deploy Automatizado - SAACB
# Uso: ./deploy.sh [backup|update|restart|logs]

set -e

# Configurações
PROJECT_NAME="projeto-saacb"
LOCAL_DIR="/data/.openclaw/workspace-dev/$PROJECT_NAME"
REMOTE_HOST="fitt@192.168.1.51"
REMOTE_DIR="/DATA/AppData/fitt/$PROJECT_NAME"
CONTAINER_NAME="saacb-django-saacb-django-1"

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "=========================================="
echo "   SAACB - Deploy Automatizado"
echo "=========================================="
echo ""

case "${1:-update}" in
  backup)
    echo -e "${YELLOW}[1/2]${NC} Criando backup local..."
    cd "$LOCAL_DIR/.."
    tar -czf "backup-$PROJECT_NAME-$(date +%Y%m%d-%H%M%S).tar.gz" "$PROJECT_NAME"
    echo -e "${GREEN}✓ Backup local criado${NC}"

    echo -e "${YELLOW}[2/2]${NC} Criando backup no servidor..."
    ssh "$REMOTE_HOST" "cd /DATA/AppData/fitt && tar -czf ${PROJECT_NAME}-backup-$(date +%Y%m%d-%H%M%S).tar.gz ${PROJECT_NAME} && ls -lh ${PROJECT_NAME}-backup-*.tar.gz | tail -1"
    echo -e "${GREEN}✓ Backup no servidor criado${NC}"
    ;;

  update)
    echo -e "${YELLOW}[1/5]${NC} Verificando status do Git..."
    cd "$LOCAL_DIR"
    git status --short
    echo -e "${GREEN}✓ Status verificado${NC}"

    echo -e "${YELLOW}[2/5]${NC} Commit e push..."
    git add -A
    git commit -m "deploy: atualização $(date +%Y-%m-%d)" || echo "Nenhuma mudança para commitar"
    git push
    echo -e "${GREEN}✓ Código enviado para GitHub${NC}"

    echo -e "${YELLOW}[3/5]${NC} Backup no servidor..."
    ssh "$REMOTE_HOST" "cd /DATA/AppData/fitt && tar -czf ${PROJECT_NAME}-backup-$(date +%Y%m%d-%H%M%S).tar.gz ${PROJECT_NAME}"
    echo -e "${GREEN}✓ Backup criado no servidor${NC}"

    echo -e "${YELLOW}[4/5]${NC} Copiando código para servidor..."
    sshpass -p '13796casa#' ssh -o StrictHostKeyChecking=no "$REMOTE_HOST" "sudo rm -rf ${REMOTE_DIR}/* 2>/dev/null || echo 'Diretório limpo'"
    sshpass -p '13796casa#' scp -r -o StrictHostKeyChecking=no "$LOCAL_DIR"/* "$REMOTE_HOST:$REMOTE_DIR/"
    echo -e "${GREEN}✓ Código copiado${NC}"

    echo -e "${YELLOW}[5/5]${NC} Reiniciando container..."
    ssh "$REMOTE_HOST" "docker restart $CONTAINER_NAME"
    sleep 5
    ssh "$REMOTE_HOST" "docker ps | grep saacb-django"
    echo -e "${GREEN}✓ Container reiniciado${NC}"
    ;;

  restart)
    echo -e "${YELLOW}[1/1]${NC} Reiniciando container..."
    ssh "$REMOTE_HOST" "docker restart $CONTAINER_NAME"
    sleep 5
    ssh "$REMOTE_HOST" "docker ps | grep saacb-django"
    echo -e "${GREEN}✓ Container reiniciado${NC}"
    ;;

  logs)
    echo -e "${YELLOW}[1/1]${NC} Exibindo logs (Ctrl+C para sair)..."
    ssh "$REMOTE_HOST" "docker logs -f $CONTAINER_NAME"
    ;;

  status)
    echo -e "${YELLOW}[1/3]${NC} Status do container..."
    ssh "$REMOTE_HOST" "docker ps | grep saacb-django"
    echo ""

    echo -e "${YELLOW}[2/3]${NC} Uso de disco..."
    ssh "$REMOTE_HOST" "df -h /DATA/AppData/fitt"
    echo ""

    echo -e "${YELLOW}[3/3]${NC} Últimos logs..."
    ssh "$REMOTE_HOST" "docker logs $CONTAINER_NAME --tail 20"
    ;;

  *)
    echo "Uso: $0 [backup|update|restart|logs|status]"
    echo ""
    echo "Comandos:"
    echo "  backup   - Criar backup local e no servidor"
    echo "  update   - Deploy completo (backup + commit + push + copiar + reiniciar)"
    echo "  restart  - Reiniciar apenas o container"
    echo "  logs     - Exibir logs em tempo real"
    echo "  status   - Mostrar status do sistema"
    exit 1
    ;;
esac

echo ""
echo -e "${GREEN}=========================================="
echo "   Deploy concluído com sucesso!"
echo "==========================================${NC}"
echo ""
