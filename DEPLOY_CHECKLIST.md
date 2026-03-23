# Checklist de Preparação para Deploy de Produção - SAACB

## ✅ Checklist de Preparação

### 1. Configurações de Segurança

- [ ] **SECRET_KEY**: Gerar nova SECRET_KEY para produção (NÃO usar `django-insecure-temporary-key`)
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

- [ ] **DEBUG = False** em produção
- [ ] **ALLOWED_HOSTS**: Configurar com domínio/IP de produção
- [ ] **HTTPS**: Configurar SSL/TLS (certificado Let's Encrypt ou Cloudflare)
- [ ] **SECURE_SSL_REDIRECT = True** (quando HTTPS estiver ativo)
- [ ] **SESSION_COOKIE_SECURE = True**
- [ ] **CSRF_COOKIE_SECURE = True**

### 2. Banco de Dados

- [ ] **SQLite** é adequado para uso pessoal/doméstico (OK)
- [ ] **PostgreSQL** recomendado para alta disponibilidade
- [ ] Fazer backup do banco de dados antes do deploy
- [ ] Verificar migrations: `python manage.py showmigrations`

### 3. Arquivos Estáticos e Mídia

- [ ] Executar `python manage.py collectstatic`
- [ ] Configurar `STATIC_ROOT` e `MEDIA_ROOT` com volumes persistentes
- [ ] WhiteNoise já configurado (✅ OK)

### 4. Environment Variables (.env)

Criar arquivo `.env` no servidor de produção:

```bash
# Django
SECRET_KEY=<nova-secret-key>
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,seu-ip.com
DATABASE_URL=sqlite:////app/data/db.sqlite3

# SISGRU (opcional)
SISGRU_USUARIO=
SISGRU_SENHA=
SISGRU_PRODUCAO=False

# Calculadora API
CALCULADORA_API_URL=http://planilha-calculos:8000
CALCULADORA_API_TOKEN=

# Ollama (opcional)
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=llama3:8b

# SSL/HTTPS
SECURE_SSL_REDIRECT=False  # Mudar para True após configurar HTTPS
```

### 5. Docker e Compose

- [ ] Verificar `Dockerfile` (✅ OK)
- [ ] Verificar `docker-compose.yml` (✅ OK)
- [ ] Arquivos docker-compose NÃO possuem o campo `version` (compatível com `docker compose`)
- [ ] Mapear volumes de forma persistente
- [ ] Configurar política de restart (`unless-stopped`)

**Comandos:**
- Antigo (v1): `docker-compose up -d`
- Novo (v2): `docker compose up -d` (recomendado)

**Nota:** Os arquivos `docker-compose.yml`, `docker-compose-dev.yml` e `docker-compose-prod.yml` não possuem o campo `version` para compatibilidade com o novo comando `docker compose`.

### 6. Servidor

#### CasaOS (Produção Atual - 192.168.1.51)

**Portas:**
- SAACB Django: 8000 (mapeado para host)

**Diretórios:**
- `/DATA/AppData/fitt/projeto-saacb/` - Código fonte
- `/DATA/AppData/fitt/projeto-saacb/data/` - Banco de dados
- `/DATA/AppData/fitt/projeto-saacb/media/` - Arquivos enviados
- `/DATA/AppData/fitt/projeto-saacb/static/` - Arquivos estáticos

**Comandos de Deploy:**
```bash
# 1. Backup antes do deploy
tar -czf projeto-saacb-backup-$(date +%Y%m%d-%H%M%S).tar.gz projeto-saacb

# 2. Parar container
docker stop saacb-django-saacb-django-1

# 3. Copiar código
scp -r projeto-saacb/* fitt@192.168.1.51:/DATA/AppData/fitt/projeto-saacb/

# 4. Iniciar container
docker start saacb-django-saacb-django-1
```

#### Oracle Cloud (Produção Futura - 144.22.225.135)

**Recursos:**
- IP: 144.22.225.135
- OS: Ubuntu
- Container: site-monitor

**Configurações necessárias:**
- [ ] Instalar Docker e Docker Compose
- [ ] Configurar firewall (portas 80, 443, 8000)
- [ ] Configurar domínio e DNS
- [ ] Configurar HTTPS (nginx + certbot ou Cloudflare)
- [ ] Configurar backup automático do banco de dados

### 7. Logs e Monitoramento

- [ ] Verificar logs: `docker logs -f saacb-django-saacb-django-1`
- [ ] Configurar rotação de logs
- [ ] Configurar alertas de erros
- [ ] Monitorar uso de CPU/memória

### 8. Backup e Recuperação

- [ ] Backup diário do banco de dados
- [ ] Backup do código fonte (git)
- [ ] Backup de arquivos media
- [ ] Testar restore de backup

**Script de Backup (exemplo):**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="/DATA/AppData/fitt/backups"

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
cp /DATA/AppData/fitt/projeto-saacb/data/db.sqlite3 $BACKUP_DIR/db-$DATE.sqlite3

# Backup do código (opcional, já está no git)
tar -czf $BACKUP_DIR/code-$DATE.tar.gz /DATA/AppData/fitt/projeto-saacb/

# Manter apenas os últimos 7 dias
find $BACKUP_DIR -name "db-*.sqlite3" -mtime +7 -delete
find $BACKUP_DIR -name "code-*.tar.gz" -mtime +7 -delete
```

### 9. Atualizações e Manutenção

- [ ] Pull do GitHub antes de cada deploy
- [ ] Verificar migrations: `python manage.py makemigrations`
- [ ] Executar migrations: `python manage.py migrate`
- [ ] Testar em ambiente de staging antes da produção

### 10. Testes

- [ ] Testar funcionalidades principais
- [ ] Testar upload de arquivos
- [ ] Testar cálculos
- [ ] Testar dashboard
- [ ] Testar login/logout

---

## 🚀 Deploy Rápido (CasaOS)

```bash
# 1. Fazer backup local
cd /data/.openclaw/workspace-dev/projeto-saacb
tar -czf ../backup-$(date +%Y%m%d).tar.gz .

# 2. Commit e push
git add -A
git commit -m "deploy: preparando para produção"
git push

# 3. Backup no servidor
ssh fitt@192.168.1.51 "cd /DATA/AppData/fitt && tar -czf projeto-saacb-backup-$(date +%Y%m%d-%H%M%S).tar.gz projeto-saacb"

# 4. Copiar código
scp -r * fitt@192.168.1.51:/DATA/AppData/fitt/projeto-saacb/

# 5. Reiniciar container
ssh fitt@192.168.1.51 "docker restart saacb-django-saacb-django-1"

# 6. Verificar logs
ssh fitt@192.168.1.51 "docker logs -f saacb-django-saacb-django-1"
```

---

## 📝 Notas

- O sistema atual usa **SQLite**, que é adequado para uso doméstico
- **WhiteNoise** já está configurado para servir arquivos estáticos
- **Gunicorn** configurado com 3 workers
- O projeto está **pronto para deploy** no CasaOS (192.168.1.51)
- Para deploy externo (Oracle Cloud), é necessário configurar HTTPS

---

**Última atualização:** 2026-03-23
**Status:** 🟢 Pronto para deploy (CasaOS)
