#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
sys.path.insert(0, '/data/.openclaw/workspace-dev/projeto-saacb')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_saacb.settings')

# Importar Django
django.setup()

# Imports após Django setup
from tarefas.models import tarefassamc
from tarefas.integracao import (
    CalculadoraClient,
    BeneficiarioData,
    CreditoData,
    IndiceData,
    tarefa_para_calculo,
    gerar_indices_padrao_dummy
)

# Cores
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
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

def main():
    print(f"\n{BLUE}{'='*60}")
    print(f"{'TESTE DE INTEGRAÇÃO SAACB ↔ PLANILHA CÁLCULOS':^60}")
    print(f"{'='*60}{RESET}")
    
    testes_passados = 0
    testes_totais = 5
    
    # 1. Testar API
    print_header("TESTE 1: API de Cálculos")
    try:
        client = CalculadoraClient()
        if client.ping():
            print_success("API está online e respondendo")
            testes_passados += 1
        else:
            print_error("API não está respondendo")
    except Exception as e:
        print_error(f"Erro ao conectar com API: {e}")
    
    # 2. Testar conversão de tarefa
    print_header("TESTE 2: Conversão de Tarefa")
    try:
        tarefas = tarefassamc.objects.all()
        if tarefas.exists():
            tarefa = tarefas.first()
            beneficiario, creditos = tarefa_para_calculo(tarefa)
            print_success(f"Conversão realizada com sucesso!")
            print(f"   Tarefa ID: {tarefa.id}")
            print(f"   Beneficiário: {beneficiario.nome_titular}")
            print(f"   NB: {beneficiario.numero_beneficio}")
            print(f"   Créditos encontrados: {len(creditos)}")
            testes_passados += 1
        else:
            print_warning("Nenhuma tarefa encontrada no banco de dados")
    except Exception as e:
        print_error(f"Erro na conversão: {e}")
    
    # 3. Testar cálculo completo
    print_header("TESTE 3: Cálculo Completo")
    try:
        client = CalculadoraClient()
        
        # Criar dados de teste
        beneficiario = BeneficiarioData(
            numero_beneficio="1247744709",
            nome_titular="ANA MARIA VIEIRA SOARES",
            periodo_debito_inicio="2002-07",
            periodo_debito_fim="2002-12",
            is_recebimento_indevido=False
        )
        
        creditos = [
            CreditoData(
                competencia="07/2002",
                periodo_inicio="08/09/2002",
                periodo_fim="08/09/2002",
                valor_original=6533.33
            )
        ]
        
        # Usar índices dummy para teste
        indices = gerar_indices_padrao_dummy()
        
        # Calcular
        resultado = client.calcular(beneficiario, creditos, indices)
        
        print_success("Cálculo realizado com sucesso!")
        print(f"   ID: {resultado.id}")
        print(f"   Total Original: R$ {resultado.total_original:.2f}")
        print(f"   Total Corrigido: R$ {resultado.total_corrigido:.2f}")
        print(f"   Diferença: R$ {resultado.diferenca:.2f}")
        testes_passados += 1
    except Exception as e:
        print_error(f"Erro no cálculo: {e}")
    
    # 4. Testar geração de PDF
    print_header("TESTE 4: Geração de PDF")
    try:
        client = CalculadoraClient()
        
        # Recalcular para obter resultado
        indices = gerar_indices_padrao_dummy()
        resultado = client.calcular(beneficiario, creditos, indices)
        
        pdf_content = client.gerar_pdf(resultado)
        
        print_success(f"PDF gerado! Tamanho: {len(pdf_content)} bytes")
        testes_passados += 1
    except Exception as e:
        print_error(f"Erro ao gerar PDF: {e}")
    
    # 5. Testar geração de Excel
    print_header("TESTE 5: Geração de Excel")
    try:
        client = CalculadoraClient()
        
        excel_content = client.gerar_excel(resultado)
        
        print_success(f"Excel gerado! Tamanho: {len(excel_content)} bytes")
        testes_passados += 1
    except Exception as e:
        print_error(f"Erro ao gerar Excel: {e}")
    
    # Resumo
    print_header("RESUMO DOS TESTES")
    
    if testes_passados == testes_totais:
        print(f"{GREEN}🎉 TODOS OS TESTES PASSARAM! ({testes_passados}/{testes_totais}){RESET}")
        print("\n✨ Integração está funcionando corretamente!")
        print("\nPróximos passos:")
        print("1. Configure índices na API: http://192.168.1.51:8002")
        print("2. Teste cálculo em uma tarefa via Django admin")
        print("3. Adicione botão de cálculo na interface de tarefas")
        return 0
    else:
        print(f"{YELLOW}⚠️  ALGUNS TESTES FALHARAM ({testes_passados}/{testes_totais}){RESET}")
        print("\nVerifique os erros acima e corrija os problemas.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
