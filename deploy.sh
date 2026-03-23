#!/bin/bash

################################################################################
# SCRIPT DE DEPLOYMENT - SAACB Django (VERSÃO COMPLETA)
# Repositório: https://github.com/profdarlan/projeto-saacb.git
# Uso: ./deploy.sh [deploy|update|rollback|logs|status|shell|backup]
################################################################################

set -e

PROJECT_DIR="/DATA/AppData/saacbdjango"
CONTAINER_NAME="saacb-django"
BACKUP_DIR="${PROJECT_DIR}/backups"
LOG_DIR="${PROJECT_DIR}/logs"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

mkdir -p "${BACKUP_DIR}" "${LOG_DIR}"

log_info() { echo -e "${BLUE}[INFO] ${1}${NC}"; }
log_success() { echo -e "${GREEN}[OK] ${1}${NC}"; }
log_warning() { echo -e "${YELLOW}[WARN] ${1}${NC}"; }
log_error() { echo -e "${RED}[ERROR] ${1}${NC}"; }

fix_permissions() {
    log_info "🔒 Fix permissões..."
    sudo chown -R casaos:devmon "${PROJECT_DIR}" 2>/dev/null || true
    sudo chmod -R 777 "${PROJECT_DIR}/db.sqlite3" "${PROJECT_DIR}/data" 2>/dev/null || true
    sudo chmod -R 755 "${PROJECT_DIR}"
    log_success "Permissões OK"
}
backup_db() {
    log_info "💾 Backup banco de dados..."
    if [ -f "${PROJECT_DIR}/db.sqlite3" ]; then
        cp "${PROJECT_DIR}/db.sqlite3" "${BACKUP_DIR}/db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
        log_success "Backup: ${BACKUP_DIR}/db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
    else
        log_warning "db.sqlite3 não encontrado"
    fi
}

stop_container() {
    log_info "⏹️  Parando container..."
    cd "${PROJECT_DIR}"
    docker compose down
    sleep 2
    log_success "Container parado"
}

update_code() {
    log_info "📥 Atualizando código..."
    cd "${PROJECT_DIR}"
    git fetch origin && git checkout main && git pull origin main
    log_success "Código atualizado"
}

start_container() {
    log_info "🐳 Iniciando container..."
    cd "${PROJECT_DIR}"
    docker compose up -d
    sleep 5
    log_success "Container iniciado"
}

run_migrations() {
    log_info "🔄 Aplicando migrations..."
    #cd "${PROJECT_DIR}"
    docker exec "${CONTAINER_NAME}" python manage.py makemigrations --noinput
    docker exec "${CONTAINER_NAME}" python manage.py migrate --noinput
    log_success "Migrations OK"
}

collect_static() {
    log_info "📁 Coletando static files..."
    #cd "${PROJECT_DIR}"
    docker exec "${CONTAINER_NAME}" python manage.py collectstatic --noinput --clear
    log_success "Static files OK"
}

health_check() {
    log_info "🔍 Health check..."
    sleep 3
    if curl -f http://localhost:8000/admin/ >/dev/null 2>&1; then
        log_success "✅ Aplicação OK!"
        return 0
    else
        log_error "❌ Aplicação DOWN"
        docker compose logs --tail 50 "${CONTAINER_NAME}"
        return 1
    fi
}
update_turbo() {
    log_info "⚡ UPDATE TURBO (30s)"
    
    # 1. Git (5s)
    git pull origin master
    
    # 2. Rebuild RÁPIDO (cache layers)
    docker compose build --no-cache=false  # Cache = rápido
    
    # 3. Restart (2s)
    docker compose up -d
    
    # 4. Migrations + static (10s)
    docker compose exec saacb-django python manage.py migrate --noinput
    docker compose exec saacb-django python manage.py collectstatic --noinput
    
    health_check
}
deploy_radical() {
    echo ""
    log_info "══════════════════════════════════════"
    log_info "🚀 DEPLOY RADICAL"
    log_info "══════════════════════════════════════"
    
    fix_permissions
    # 1. Git (5s)
    git pull origin master
    
    # 2. Rebuild COMPLETO (no cache)
    docker compose build --no-cache=true  # No cache = completo
    
    # 3. Restart (2s)
    docker compose up -d
    
    # 4. Migrations + static (10s)
    docker compose exec saacb-django python manage.py migrate --noinput
    docker compose exec saacb-django python manage.py collectstatic --noinput
    
    health_check
}

deploy() {
    echo ""
    log_info "══════════════════════════════════════"
    log_info "🚀 DEPLOY COMPLETO"
    log_info "══════════════════════════════════════"
    fix_permissions
    backup_db
    stop_container
    update_code
    start_container
    run_migrations
    collect_static
    health_check
    echo ""
    log_success "🎉 DEPLOY CONCLUÍDO!"
}

update() {
    log_info "📥 UPDATE RÁPIDO"
    update_code
    docker compose restart
    sleep 3
    run_migrations
    collect_static
    health_check
}

rollback() {
    log_warning "⏮️  ROLLBACK"
    stop_container
    cd "${PROJECT_DIR}"
    git reset --hard HEAD~1
    start_container
    run_migrations
    collect_static
    health_check
}

status() {
    echo ""
    log_info "📊 STATUS"
    cd "${PROJECT_DIR}"
    echo "Container:"
    docker compose ps
    echo "Git:"
    git branch --show-current
    git log --oneline -3
    echo "Backups:"
    ls -lht "${BACKUP_DIR}" | head -4
    health_check
}

logs() {
    cd "${PROJECT_DIR}"
    docker compose logs -f "${CONTAINER_NAME}"
}

shell() {
    cd "${PROJECT_DIR}"
    docker exec -it "${CONTAINER_NAME}" bash
}

help() {
    cat << 'HELP'
🚀 DEPLOYMENT SAACB Django

COMANDOS:
  deploy    🚀 Deploy completo (7 etapas)
  update    📥 Update rápido
  rollback  ⏮️  Reverter
  status    📊 Status
  logs      📋 Logs
  shell     🔧 Shell
  backup    💾 Backup BD
  help      ❓ Ajuda

EXEMPLO:
  ./deploy.sh deploy

PASTAS:
  Projeto: /DATA/AppData/saacbdjango
  Backup:  /DATA/AppData/saacbdjango/backups
HELP
}

case "${1:-help}" in
    deploy) deploy ;;
    deploy_radical) deploy_radical ;;
    update) update ;;
    update_turbo) update_turbo ;;
    rollback) rollback ;;
    status) status ;;
    logs) logs ;;
    shell) shell ;;
    backup) backup_db ;;
    help|-h|--help) help ;;
    *) log_error "Comando inválido: ${1}"; help; exit 1 ;;
esac