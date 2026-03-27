"""
Proxy para API de Cálculos
Resolve problema de Mixed Content (HTTPS → HTTP)
"""

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
import json

# Configuração da API externa (Cloudflare Tunnel)
API_BASE_URL = "https://calculadora.lakeserver.online/api/"
API_TOKEN = "9764f2d2227e0f498ae5ebc39bdaba5dfafc4443dde7aa26df9c87a4a8c5d7f1"


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_proxy(request, path):
    """
    Proxy para API de Cálculos
    Redireciona requisições HTTPS do SAACB para HTTP da API local
    """

    # Construir URL completa da API (sem duplicar /api)
    api_url = f"{API_BASE_URL}{path}"

    # Preparar headers (simples, evitar compressão e problemas)
    headers = {
        'Content-Type': request.content_type or 'application/json',
        'X-API-TOKEN': API_TOKEN,
        'Accept-Encoding': 'identity'  # Evita compressão para facilitar parse JSON
    }

    response = None
    try:
        # Fazer a requisição para a API
        if request.method == 'GET':
            response = requests.get(api_url, headers=headers, params=request.GET.dict(), timeout=30)
        else:  # POST
            response = requests.post(
                api_url,
                headers=headers,
                data=request.body,
                params=request.GET.dict(),
                timeout=60
            )

        # Debug: imprimir status e URL
        print(f"Proxy: {request.method} {api_url} -> {response.status_code}")

        # Retornar resposta JSON
        try:
            return JsonResponse(
                response.json(),
                status=response.status_code,
                safe=False,
                json_dumps_params={'ensure_ascii': False}
            )
        except json.JSONDecodeError:
            # Se não for JSON, retorna o conteúdo como texto
            return HttpResponse(
                response.content,
                status=response.status_code,
                content_type=response.headers.get('Content-Type', 'text/plain')
            )

    except requests.RequestException as e:
        return JsonResponse(
            {'error': f'Erro ao conectar com API: {str(e)}'},
            status=503
        )
