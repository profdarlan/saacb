#!/usr/bin/env python3
"""
Diagnóstico Completo do Sistema SAACB
Verifica todos os componentes e reporta o status
"""
import os
import sys
import django
import subprocess
from pathlib import Path

# Cores
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{CYAN}ℹ️  {text}{RESET}")

def check_file(path, description):
    """Verifica se arquivo existe"""
    if os.path.exists(path):
        print_success(f"{description}: {path}")
        return True
    else:
        print_error(f"{description} não encontrado: {path}")
        return False

def check_import(module_name, description):
    """Verifica se módulo pode ser importado"""
    try:
        __import__(module_name)
        print_success(f"{description}: {module_name}")
        return True
    except ImportError as e:
        print_error(f"{description}: {module_name} - {e}")
        return False

def main():
    """Executa diagnóstico completo"""
    print(f"\n{BLUE}{'='*60}")
    print(f"{'DIAGNÓSTICO COMPLETO SAACB':^60}")
    print(f"{'='*60}{RESET}")
    
    total_checks = 0
    passed_checks = 0
    
    # 1. Estrutura de Arquivos
    print_header("1. ESTRUTURA DE ARQUIVOS")
    
    files_to_check = [
        ('/data/.openclaw/workspace-dev/projeto-saacb/manage.py', 'manage.py'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/projeto_saacb/settings.py', 'settings.py'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/projeto_saacb/urls.py', 'urls.py'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/tarefas/models.py', 'models.py'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/tarefas/views.py', 'views.py'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/tarefas/urls.py', 'tarefas/urls.py'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/tarefas/admin.py', 'admin.py'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/tarefas/gru/gru_service.py', 'gru_service.py'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/tarefas/integracao/calculadora_client.py', 'calculadora_client.py'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/tarefas/views_integracao.py', 'views_integracao.py'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/.env', '.env'),
        ('/data/.openclaw/workspace-dev/projeto-saacb/db.sqlite3', 'Database (SQLite)'),
    ]
    
    for path, desc in files_to_check:
        total_checks += 1
        if check_file(path, desc):
            passed_checks += 1
    
    # 2. Python e Dependências
    print_header("2. PYTHON E DEPENDÊNCIAS")
    
    python_version = sys.version_info
    print_info(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    deps_to_check = [
        ('django', 'Django'),
        ('requests', 'Requests'),
        ('reportlab', 'ReportLab'),
        ('dotenv', 'python-dotenv'),
    ]
    
    for module, desc in deps_to_check:
        total_checks += 1
        if check_import(module, desc):
            passed_checks += 1
    
    # 3. Configuração Django
    print_header("3. CONFIGURAÇÃO DJANGO")
    
    os.chdir('/data/.openclaw/workspace-dev/projeto-saacb')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_saacb.settings')
    
    try:
        import django
        django.setup()
        print_success("Django configurado com sucesso")
        total_checks += 1
        passed_checks += 1
    except Exception as e:
        print_error(f"Erro ao configurar Django: {e}")
        total_checks += 1
    
    # 4. Migrations
    print_header("4. MIGRATIONS")
    
    try:
        result = subprocess.run(
            ['python3', 'manage.py', 'showmigrations'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success("Migrations verificadas")
            lines = result.stdout.split('\n')
            applied = len([l for l in lines if '[X]' in l])
            print_info(f"Total aplicadas: {applied}")
            total_checks += 1
            passed_checks += 1
        else:
            print_error("Erro ao verificar migrations")
            total_checks += 1
    except Exception as e:
        print_error(f"Erro ao verificar migrations: {e}")
        total_checks += 1
    
    # 5. Models e Aplicações
    print_header("5. MODELS E APLICAÇÕES")
    
    try:
        from tarefas.models import (
            tarefassamc,
            GRU,
            Role,
            UserProfile
        )
        print_success("Models importados com sucesso")
        total_checks += 1
        passed_checks += 1
        
        # Contar registros
        tarefa_count = tarefassamc.objects.count()
        gru_count = GRU.objects.count()
        
        print_info(f"Tarefas no banco: {tarefa_count}")
        print_info(f"GRUs no banco: {gru_count}")
        
    except Exception as e:
        print_error(f"Erro ao importar models: {e}")
        total_checks += 1
    
    # 6. Integração SISGRU
    print_header("6. INTEGRAÇÃO SISGRU")
    
    try:
        from tarefas.gru.gru_service import SISGRUService
        print_success("SISGRU Service importado")
        total_checks += 1
        passed_checks += 1
        
        # Verificar configuração
        from django.conf import settings
        sisgru_user = getattr(settings, 'SISGRU_USUARIO', None)
        sisgru_prod = getattr(settings, 'SISGRU_PRODUCAO', False)
        
        if sisgru_user and sisgru_user != 'seu_usuario':
            print_success(f"SISGRU configurado (produção: {sisgru_prod})")
        else:
            print_warning("SISGRU não configurado (usando valores padrão)")
        
    except Exception as e:
        print_error(f"Erro na integração SISGRU: {e}")
        total_checks += 1
    
    # 7. Integração Calculadora
    print_header("7. INTEGRAÇÃO CALCULADORA")
    
    try:
        from tarefas.integracao import CalculadoraClient
        print_success("CalculadoraClient importado")
        total_checks += 1
        passed_checks += 1
        
        # Verificar API
        client = CalculadoraClient()
        if client.ping():
            print_success("API de cálculos está online")
            total_checks += 1
            passed_checks += 1
            
            # Verificar índices
            indices = client.obter_indices_padrao()
            if indices:
                print_success(f"Índices configurados: {len(indices)} competências")
            else:
                print_warning("Nenhum índice configurado")
        else:
            print_warning("API de cálculos está offline")
            total_checks += 1
        
    except Exception as e:
        print_error(f"Erro na integração calculadora: {e}")
        total_checks += 1
    
    # 8. URLs e Rotas
    print_header("8. URLS E ROTAS")
    
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        urls_list = []
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                for sub_pattern in pattern.url_patterns:
                    urls_list.append(str(sub_pattern.pattern))
            else:
                urls_list.append(str(pattern.pattern))
        
        print_info(f"Total de rotas: {len(urls_list)}")
        print(f"  Exemplos: {', '.join(urls_list[:5])}")
        
        total_checks += 1
        passed_checks += 1
    except Exception as e:
        print_error(f"Erro ao verificar URLs: {e}")
        total_checks += 1
    
    # 9. Templates Estáticos
    print_header("9. TEMPLATES E ESTÁTICOS")
    
    templates_to_check = [
        'templates/base.html',
        'templates/design-system/button.html',
        'tarefas/templates/tarefas/integracao/calcular_creditos.html',
    ]
    
    for template in templates_to_check:
        total_checks += 1
        if check_file(f'/data/.openclaw/workspace-dev/projeto-saacb/{template}', template):
            passed_checks += 1
    
    # 10. Sistema Check
    print_header("10. SISTEMA CHECK (DJANGO)")
    
    try:
        result = subprocess.run(
            ['python3', 'manage.py', 'check'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success("Django check sem erros")
            if 'issues' in result.stdout:
                print_info(result.stdout.strip())
            total_checks += 1
            passed_checks += 1
        else:
            print_error("Django check encontrou problemas:")
            print(result.stderr)
            total_checks += 1
    except Exception as e:
        print_error(f"Erro ao executar Django check: {e}")
        total_checks += 1
    
    # Resumo
    print_header("RESUMO DO DIAGNÓSTICO")
    
    percentage = (passed_checks / total_checks * 100) if total_checks > 0 else 0
    
    print(f"Total de Verificações: {total_checks}")
    print(f"Verificações Aprovadas: {passed_checks}")
    print(f"Verificações Falhadas: {total_checks - passed_checks}")
    print(f"\nTaxa de Sucesso: {percentage:.1f}%")
    
    if percentage >= 90:
        print(f"\n{GREEN}🎉 SISTEMA EM BOM ESTADO!{RESET}")
        return 0
    elif percentage >= 70:
        print(f"\n{YELLOW}⚠️  SISTEMA FUNCIONAL COM ALGUNS AVISOS{RESET}")
        return 1
    else:
        print(f"\n{RED}❌ SISTEMA COM PROBLEMAS - REVISAR{RESET}")
        return 2

if __name__ == '__main__':
    sys.exit(main())
