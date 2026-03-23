#!/bin/bash
# Script para corrigir o erro de migrations no Docker

echo "========================================="
echo "CORRIGINDO MIGRATIONS DOCKER SAACB"
echo "========================================="
echo ""

# Verificar se Docker está rodando
if ! docker ps &> /dev/null; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

# Nome do container (ajuste se necessário)
CONTAINER_NAME="saacb-django-teste"

echo "1. Parando container..."
docker stop $CONTAINER_NAME 2>/dev/null || echo "   Container não estava rodando"

echo ""
echo "2. Removendo container..."
docker rm $CONTAINER_NAME 2>/dev/null || echo "   Container não existia"

echo ""
echo "3. Recriando imagem Docker..."
docker-compose build

echo ""
echo "4. Subindo novo container..."
docker-compose up -d

echo ""
echo "5. Aguardando inicialização..."
sleep 10

echo ""
echo "6. Verificando logs..."
docker logs $CONTAINER_NAME --tail 50

echo ""
echo "========================================="
echo "✅ CORREÇÃO CONCLUÍDA!"
echo "========================================="
echo ""
echo "Acesse: http://192.168.1.51:30010"
echo ""
echo "Se o erro persistir, execute:"
echo "  docker exec -it $CONTAINER_NAME python fix-migrations.py"
echo ""
