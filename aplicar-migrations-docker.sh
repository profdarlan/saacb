#!/bin/bash
# Script para aplicar migrations no container Docker SAACB

set -e

echo "========================================="
echo "APLICANDO MIGRATIONS DOCKER SAACB"
echo "========================================="
echo ""

CONTAINER="saacb-django-teste"

# 1. Verificar se o container está rodando
if ! docker ps | grep -q $CONTAINER; then
    echo "❌ Container $CONTAINER não está rodando"
    echo ""
    echo "Inicie o container primeiro:"
    echo "  docker start $CONTAINER"
    echo "  ou"
    echo "  docker-compose up -d"
    exit 1
fi

echo "✅ Container $CONTAINER está rodando"
echo ""

# 2. Verificar se o arquivo fix-migrations.py existe no container
echo "2. Verificando se fix-migrations.py existe no container..."
if ! docker exec $CONTAINER ls /app/fix-migrations.py &>/dev/null; then
    echo "⚠️  fix-migrations.py não encontrado no container"
    echo "   Copiando do host para o container..."
    
    docker cp /data/.openclaw/workspace-dev/projeto-saacb/fix-migrations.py $CONTAINER:/app/fix-migrations.py
    echo "   ✅ Arquivo copiado"
else
    echo "   ✅ fix-migrations.py encontrado"
fi
echo ""

# 3. Aplicar migrations
echo "3. Aplicando migrations..."
docker exec $CONTAINER python manage.py migrate --noinput
echo "   ✅ Migrations aplicadas"
echo ""

# 4. Verificar migrations aplicadas
echo "4. Verificando migrations aplicadas..."
docker exec $CONTAINER python manage.py showmigrations tarefas | grep "0015_integracao_calculadora"
echo ""

# 5. Reiniciar container
echo "5. Reiniciando container..."
docker restart $CONTAINER
echo "   ✅ Container reiniciado"
echo ""

# 6. Aguardar container iniciar
echo "6. Aguardando container iniciar..."
sleep 5
echo "   ✅ Container iniciado"
echo ""

# 7. Verificar logs
echo "7. Verificando logs iniciais..."
docker logs $CONTAINER --tail 20
echo ""

echo "========================================="
echo "✅ MIGRATIONS APLICADAS!"
echo "========================================="
echo ""
echo "Acesse o sistema:"
echo "  http://192.168.1.51:30010/tarefas/"
echo ""
echo "Se o erro persistir, verifique:"
echo "  docker logs $CONTAINER --tail 50"
echo ""
