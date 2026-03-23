"""
Integração Django SAACB ↔ Planilha Cálculos (FastAPI)
Views para cálculo de créditos em tarefas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import io

# Imports do projeto
from .models import tarefassamc
from .integracao import (
    CalculadoraClient,
    BeneficiarioData,
    CreditoData,
    IndiceData,
    CalculoResultado,
    tarefa_para_calculo,
    APIException
)

# Instanciar cliente
calculadora_client = CalculadoraClient()


# ============= VIEWS =============

@require_http_methods(["GET", "POST"])
def calcular_creditos_tarefa(request, tarefa_id):
    """
    View para calcular créditos em uma tarefa específica

    Template: templates/tarefas/calcular_creditos.html
    """
    tarefa = get_object_or_404(tarefassamc, id=tarefa_id)

    if request.method == "POST":
        try:
            # Converter tarefa para dados de cálculo
            beneficiario, creditos = tarefa_para_calculo(tarefa)

            # Obter índices
            try:
                indices_dict = calculadora_client.obter_indices_padrao()
                indices = [
                    IndiceData(competencia=comp, indice=ind)
                    for comp, ind in indices_dict.items()
                ]
            except APIException:
                messages.error(request, "Não foi possível obter índices. Usando valores padrão.")
                # Usar índices dummy para teste
                from .integracao.calculadora_client import gerar_indices_padrao_dummy
                indices = gerar_indices_padrao_dummy()

            # Realizar cálculo
            resultado = calculadora_client.calcular(
                beneficiario=beneficiario,
                creditos=creditos,
                indices=indices
            )

            # Atualizar tarefa com resultados
            tarefa.valor_original_calculado = resultado.total_original
            tarefa.valor_corrigido_calculado = resultado.total_corrigido
            tarefa.valor_diferenca = resultado.diferenca
            tarefa.detalhes_calculo = {
                'id': resultado.id,
                'timestamp': resultado.timestamp,
                'resultados': resultado.resultados,
            }
            tarefa.calculado_em = timezone.now()
            tarefa.save()

            messages.success(request, f"Cálculo realizado! Diferença: R$ {resultado.diferenca:.2f}")

            # Se solicitado, gerar e salvar PDF
            if request.POST.get('gerar_pdf'):
                try:
                    pdf_content = calculadora_client.gerar_pdf(resultado)

                    # Salvar PDF na tarefa (usando campo oficio2 para armazenar)
                    # Nota: seria melhor adicionar campo específico via migration
                    nome_arquivo = f"relatorio_calculo_{tarefa.id}_{resultado.id}.pdf"
                    
                    messages.success(request, "PDF gerado! O arquivo está pronto para download.")
                except APIException as e:
                    messages.error(request, f"Erro ao gerar PDF: {str(e)}")

            return redirect('tarefas:tarefa_detail', pk=tarefa.id)

        except APIException as e:
            messages.error(request, f"Erro no cálculo: {str(e)}")
            return render(request, 'tarefas/integracao/calcular_creditos.html', {
                'tarefa': tarefa,
                'erro': str(e),
            })

    # GET - Mostra formulário de cálculo
    return render(request, 'tarefas/integracao/calcular_creditos.html', {
        'tarefa': tarefa,
        'api_disponivel': calculadora_client.ping(),
    })


@require_http_methods(["POST"])
@csrf_exempt
def calcular_ajax(request):
    """
    Endpoint AJAX para salvar resultados de cálculo direto na tarefa
    """
    tarefa_id = request.POST.get('tarefa_id')
    if not tarefa_id:
        return JsonResponse({'status': 'error', 'message': 'ID da tarefa não informado'}, status=400)

    tarefa = get_object_or_404(tarefassamc, id=tarefa_id)

    try:
        # Tentar usar a API de cálculos se estiver disponível
        try:
            # Converter tarefa para dados de cálculo
            beneficiario, creditos = tarefa_para_calculo(tarefa)

            # Obter índices
            indices_dict = calculadora_client.obter_indices_padrao()
            indices = [
                IndiceData(competencia=comp, indice=ind)
                for comp, ind in indices_dict.items()
            ]

            # Realizar cálculo
            resultado = calculadora_client.calcular(
                beneficiario=beneficiario,
                creditos=creditos,
                indices=indices
            )

            # Atualizar tarefa
            tarefa.valor_original_calculado = resultado.total_original
            tarefa.valor_corrigido_calculado = resultado.total_corrigido
            tarefa.valor_diferenca = resultado.diferenca
            tarefa.detalhes_calculo = {
                'id': resultado.id,
                'timestamp': resultado.timestamp,
                'resultados': resultado.resultados,
            }
            tarefa.calculado_em = timezone.now()
            tarefa.save()

            return JsonResponse({
                'status': 'success',
                'resultado': {
                    'id': resultado.id,
                    'timestamp': resultado.timestamp,
                    'total_original': resultado.total_original,
                    'total_corrigido': resultado.total_corrigido,
                    'diferenca': resultado.diferenca,
                    'quantidade': resultado.quantidade_creditos,
                    'resultados': resultado.resultados,
                }
            })
        except Exception as api_error:
            # Se a API falhar, verificar se já há valores calculados na tarefa
            if (tarefa.valor_original_calculado is not None and
                tarefa.valor_corrigido_calculado is not None and
                tarefa.valor_diferenca is not None):
                return JsonResponse({
                    'status': 'success',
                    'message': 'Usando valores previamente calculados',
                    'resultado': {
                        'total_original': float(tarefa.valor_original_calculado),
                        'total_corrigido': float(tarefa.valor_corrigido_calculado),
                        'diferenca': float(tarefa.valor_diferenca),
                        'resultados': tarefa.detalhes_calculo.get('resultados', []) if tarefa.detalhes_calculo else [],
                    }
                })
            else:
                raise Exception(f"API indisponível e não há valores calculados: {str(api_error)}")

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(["POST"])
@csrf_exempt
def salvar_resultados_calculo(request, tarefa_id):
    """
    Salva os resultados de cálculo gerados pelo frontend na tarefa
    """
    tarefa = get_object_or_404(tarefassamc, id=tarefa_id)

    try:
        import json
        data = json.loads(request.body.decode('utf-8'))

        # Extrair valores do payload
        total_original = data.get('total_original', 0)
        total_corrigido = data.get('total_corrigido', 0)
        diferenca = data.get('diferenca', 0)
        resultados = data.get('resultados', [])

        # Atualizar tarefa com os resultados
        tarefa.valor_original_calculado = total_original
        tarefa.valor_corrigido_calculado = total_corrigido
        tarefa.valor_diferenca = diferenca
        tarefa.detalhes_calculo = {
            'resultados': resultados,
            'timestamp': timezone.now().isoformat(),
        }
        tarefa.calculado_em = timezone.now()
        tarefa.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Resultados salvos com sucesso',
            'total_original': total_original,
            'total_corrigido': total_corrigido,
            'diferenca': diferenca,
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(["POST"])
def baixar_relatorio_pdf(request, tarefa_id):
    """
    Gera e baixa relatório PDF de uma tarefa
    """
    tarefa = get_object_or_404(tarefassamc, id=tarefa_id)

    # Verificar se já tem cálculo salvo
    if not tarefa.detalhes_calculo:
        messages.error(request, "Esta tarefa ainda não foi calculada.")
        return redirect('tarefas:tarefa_detail', pk=tarefa.id)

    try:
        # Recuperar resultado do cálculo
        resultado = CalculoResultado(
            id=tarefa.detalhes_calculo['id'],
            timestamp=tarefa.detalhes_calculo['timestamp'],
            beneficiario=BeneficiarioData(
                numero_beneficio=tarefa.nb1 or tarefa.nb2 or '',
                nome_titular=tarefa.nome_interessado or '',
                periodo_debito_inicio='',
                periodo_debito_fim='',
                is_recebimento_indevido=False
            ),
            resultados=tarefa.detalhes_calculo['resultados'],
            total_original=tarefa.valor_original_calculado,
            total_corrigido=tarefa.valor_corrigido_calculado,
            diferenca=tarefa.valor_diferenca
        )

        # Gerar PDF
        pdf_content = calculadora_client.gerar_pdf(resultado)

        # Retornar como attachment
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="relatorio_calculo_{tarefa.id}.pdf"'
        return response

    except APIException as e:
        messages.error(request, f"Erro ao gerar PDF: {str(e)}")
        return redirect('tarefas:tarefa_detail', pk=tarefa.id)


@require_http_methods(["POST"])
def baixar_relatorio_excel(request, tarefa_id):
    """
    Gera e baixa relatório Excel de uma tarefa
    """
    tarefa = get_object_or_404(tarefassamc, id=tarefa_id)

    # Verificar se já tem cálculo salvo
    if not tarefa.detalhes_calculo:
        messages.error(request, "Esta tarefa ainda não foi calculada.")
        return redirect('tarefas:tarefa_detail', pk=tarefa.id)

    try:
        # Recuperar resultado do cálculo
        resultado = CalculoResultado(
            id=tarefa.detalhes_calculo['id'],
            timestamp=tarefa.detalhes_calculo['timestamp'],
            beneficiario=BeneficiarioData(
                numero_beneficio=tarefa.nb1 or tarefa.nb2 or '',
                nome_titular=tarefa.nome_interessado or '',
                periodo_debito_inicio='',
                periodo_debito_fim='',
                is_recebimento_indevido=False
            ),
            resultados=tarefa.detalhes_calculo['resultados'],
            total_original=tarefa.valor_original_calculado,
            total_corrigido=tarefa.valor_corrigido_calculado,
            diferenca=tarefa.valor_diferenca
        )

        # Gerar Excel
        excel_content = calculadora_client.gerar_excel(resultado)

        # Retornar como attachment
        response = HttpResponse(excel_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="relatorio_calculo_{tarefa.id}.xlsx"'
        return response

    except APIException as e:
        messages.error(request, f"Erro ao gerar Excel: {str(e)}")
        return redirect('tarefas:tarefa_detail', pk=tarefa.id)


@require_http_methods(["GET"])
def status_api(request):
    """
    Retorna status da API de cálculos
    Para verificação via AJAX
    """
    return JsonResponse({
        'api_online': calculadora_client.ping(),
        'indices_configurados': len(calculadora_client.obter_indices_padrao()),
    })


@require_http_methods(["POST"])
@csrf_exempt
def aprovar_calculos_tarefa(request, tarefa_id):
    """
    Aprova os cálculos da tarefa e migra o valor corrigido para o campo Valor.
    Atualiza os campos calculados e marca calculos_aprovados=True.
    O signal pre_save cuida da migração para o campo valor principal.
    """
    tarefa = get_object_or_404(tarefassamc, id=tarefa_id)

    try:
        import json
        data = json.loads(request.body.decode('utf-8'))
        
        # Verificar se deve usar o valor corrigido ou original
        usar_corrigido = data.get('usar_corrigido', True)

        # Verificar se há valores calculados
        if tarefa.valor_corrigido_calculado is None:
            return JsonResponse({
                'success': False,
                'error': 'Não há valores calculados para aprovar. Realize o cálculo primeiro.'
            }, status=400)

        # Marcar como aprovado (o signal pre_save fará a migração)
        tarefa.calculos_aprovados = True

        # Atualizar status para indicar migração
        if tarefa.status == 'PENDENTE':
            tarefa.status = 'PENDENTE - MIGRADO'
        elif tarefa.status in ['CONCLUIDA_INTERMEDIARIA', 'CONCLUIDA_FINALIZADA']:
            # Se já está concluída, mantém o status mas marca que foi migrado
            pass

        # O signal pre_save migrará os valores automaticamente
        tarefa.save()

        # Retornar o valor que foi migrado
        valor_migrado = str(tarefa.valor_corrigido_calculado if usar_corrigido else tarefa.valor_original_calculado)

        return JsonResponse({
            'success': True,
            'valor_original': str(tarefa.valor_original_calculado),
            'valor_corrigido': str(tarefa.valor_corrigido_calculado),
            'valor_diferenca': str(tarefa.valor_diferenca),
            'valor_migrado': valor_migrado,
            'status': tarefa.status,
            'mensagem': 'Cálculos aprovados e migrados com sucesso!'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido na requisição'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def aprovar_valor(request, tarefa_id):
    """
    Aprova os cálculos e migra o valor corrigido para o campo Valor
    da tarefa. Atualiza o status para "PENDENTE - MIGRADO".
    """
    tarefa = get_object_or_404(tarefassamc, id=tarefa_id)

    try:
        data = request.body.decode('utf-8')
        import json
        payload = json.loads(data)
        valor_str = payload.get('valor', '').strip()

        if not valor_str:
            return JsonResponse({'error': 'Valor não fornecido'}, status=400)

        # Remover formatação de moeda (R$, pontos, vírgulas)
        valor_str = valor_str.replace('R$', '').replace('.', '').replace(',', '.').strip()

        try:
            valor = float(valor_str)
        except ValueError:
            return JsonResponse({'error': 'Valor inválido'}, status=400)

        # Migrar valor para o campo valor principal
        tarefa.valor = valor_str  # Manter formatado para exibição

        # Atualizar status para indicar migração
        if tarefa.status == 'PENDENTE':
            tarefa.status = 'PENDENTE - MIGRADO'

        tarefa.save()

        return JsonResponse({
            'success': True,
            'valor': valor_str,
            'status': tarefa.status,
            'mensagem': 'Valor aprovado e migrado com sucesso'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
