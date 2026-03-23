#!/bin/bash
# Script de Setup para Docker SAACB
# Executa migrations e configura o banco de dados

set -e  # Para em caso de erro

echo "========================================="
echo "SETUP SAACB - DOCKER"
echo "========================================="
echo ""

# 1. Criar migrations pendentes (se houver mudanças)
echo "📝 1. Criando migrations..."
python manage.py makemigrations --noinput || echo "   Nenhuma migration nova"

# 2. Aplicar migrations
echo ""
echo "📦 2. Aplicando migrations..."
python manage.py migrate --noinput

# 3. Verificar migrations aplicadas
echo ""
echo "✅ 3. Verificando migrations..."
python manage.py showmigrations | grep "\[X\]" | wc -l

# 4. Criar superusuário (se não existir)
echo ""
echo "👤 4. Configurando superusuário..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
email = 'admin@saacb.local'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✓ Superusuário criado: {username}")
else:
    print(f"✓ Superusuário já existe: {username}")
EOF

# 5. Verificar sistema
echo ""
echo "🔍 5. Verificando sistema..."
python manage.py check

# 6. Coletar arquivos estáticos
echo ""
echo "📁 6. Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear || echo "   Nenhum arquivo estático para coletar"

echo ""
echo "========================================="
echo "✅ SETUP CONCLUÍDO!"
echo "========================================="
echo ""
echo "Acesse: http://localhost:30010"
echo "Admin: http://localhost:30010/admin/"
echo "Usuário: admin"
echo "Senha: admin123"
echo ""
