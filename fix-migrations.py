#!/usr/bin/env python
"""
Script para aplicar migrations específicas da integração
Usado quando migrations existentes falharam
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_saacb.settings')
django.setup()

from django.db import connection
from django.db.migrations.recorder import MigrationRecorder
from django.core.management import call_command

def main():
    print("=" * 60)
    print("APLICANDO MIGRATIONS DE INTEGRAÇÃO")
    print("=" * 60)
    print()
    
    # 1. Verificar migrations aplicadas
    print("1. Verificando migrations aplicadas...")
    recorder = MigrationRecorder.Migration.objects.filter(
        app='tarefas'
    ).order_by('name')
    
    applied = [m.name for m in recorder]
    print(f"   Migrations aplicadas: {len(applied)}")
    
    # Verificar se migration de integração está aplicada
    integracao_migration = '0015_integracao_calculadora'
    
    if integracao_migration in applied:
        print(f"   ✓ Migration {integracao_migration} já está aplicada")
    else:
        print(f"   ⚠️  Migration {integracao_migration} NÃO está aplicada")
        print()
        
        # 2. Tentar aplicar migration específica
        print(f"2. Aplicando migration {integracao_migration}...")
        try:
            call_command(
                'migrate',
                'tarefas',
                integracao_migration,
                '--fake-initial',
                verbosity=2
            )
            print(f"   ✓ Migration aplicada com sucesso")
        except Exception as e:
            print(f"   ⚠️  Erro ao aplicar migration: {e}")
            print()
            
            # 3. Tentar fake migration se o banco já tiver as colunas
            print("3. Tentando fake migration...")
            try:
                call_command(
                    'migrate',
                    'tarefas',
                    integracao_migration,
                    '--fake',
                    verbosity=2
                )
                print(f"   ✓ Fake migration aplicada")
            except Exception as e2:
                print(f"   ❌ Erro: {e2}")
                return 1
    
    print()
    
    # 4. Verificar colunas da tabela
    print("4. Verificando colunas da tabela tarefassamc...")
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='tarefas_tarefassamc'"
        )
        table = cursor.fetchone()
        
        if table:
            cursor.execute("PRAGMA table_info(tarefas_tarefassamc)")
            columns = [row[1] for row in cursor.fetchall()]
            
            required_columns = [
                'valor_original_calculado',
                'valor_corrigido_calculado',
                'valor_diferenca',
                'detalhes_calculo',
                'relatorio_pdf',
                'calculado_em'
            ]
            
            print(f"   Total de colunas: {len(columns)}")
            
            missing_columns = []
            for col in required_columns:
                if col in columns:
                    print(f"   ✓ {col}")
                else:
                    print(f"   ✗ {col} FALTANDO")
                    missing_columns.append(col)
            
            if missing_columns:
                print()
                print("5. Colunas faltando! Tentando adicionar...")
                
                for col in missing_columns:
                    try:
                        if col == 'valor_original_calculado':
                            cursor.execute(
                                "ALTER TABLE tarefas_tarefassamc "
                                "ADD COLUMN valor_original_calculado DECIMAL(12,2) NULL"
                            )
                        elif col == 'valor_corrigido_calculado':
                            cursor.execute(
                                "ALTER TABLE tarefas_tarefassamc "
                                "ADD COLUMN valor_corrigido_calculado DECIMAL(12,2) NULL"
                            )
                        elif col == 'valor_diferenca':
                            cursor.execute(
                                "ALTER TABLE tarefas_tarefassamc "
                                "ADD COLUMN valor_diferenca DECIMAL(12,2) NULL"
                            )
                        elif col == 'detalhes_calculo':
                            cursor.execute(
                                "ALTER TABLE tarefas_tarefassamc "
                                "ADD COLUMN detalhes_calculo TEXT NULL"
                            )
                        elif col == 'relatorio_pdf':
                            cursor.execute(
                                "ALTER TABLE tarefas_tarefassamc "
                                "ADD COLUMN relatorio_pdf VARCHAR(100) NULL"
                            )
                        elif col == 'calculado_em':
                            cursor.execute(
                                "ALTER TABLE tarefas_tarefassamc "
                                "ADD COLUMN calculado_em DATETIME NULL"
                            )
                        
                        print(f"   ✓ Coluna {col} adicionada")
                    except Exception as e:
                        print(f"   ✗ Erro ao adicionar {col}: {e}")
                
                connection.commit()
        
    print()
    print("=" * 60)
    print("✅ CONCLUÍDO!")
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
