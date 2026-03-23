# tarefas/utils.py
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.response import TemplateResponse

# xhtml2pdf desabilitado temporariamente devido a conflito de dependências
# from xhtml2pdf import pisa

def render_to_pdf(request, template_src, context_dict=None):
    if context_dict is None:
        context_dict = {}
    try:
        template = get_template(template_src)
        html = template.render(context_dict)
        
        # Se quiser manter fallback HTML
        return HttpResponse(html, content_type='text/html; charset=utf-8')
    except Exception as e:
        error_html = f"<h1>Erro ao renderizar relatório</h1><p>{str(e)}</p>"
        return HttpResponse(error_html, content_type='text/html; charset=utf-8', status=500)
