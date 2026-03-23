from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView,
    DeleteView, TemplateView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.db.models import Count, Q
from datetime import timedelta
import csv
import io

from .models import tarefassamc, tipo_servico, nome_motiv, conc_analise
from .forms import TarefaForm, CSVUploadForm
from .services import gerar_texto_documento
from .utils import render_to_pdf


@method_decorator(login_required, name='dispatch')
class TarefaListView(ListView):
    model = tarefassamc
    template_name = 'tarefas/tarefa_list.html'
    context_object_name = 'tarefas'

    def get_queryset(self):
        queryset = tarefassamc.objects.filter(assigned_user=self.request.user)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(nome_interessado__icontains=q) |
                Q(servico__icontains=q) |
                Q(status__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        all_tarefas = tarefassamc.objects.filter(assigned_user=user)

        STATUS_CONCLUIDOS = ['CONCLUIDA_INTERMEDIARIA', 'CONCLUIDA_FINALIZADA']

        pendentes = all_tarefas.exclude(status__in=STATUS_CONCLUIDOS).count()
        concluidas = all_tarefas.filter(status__in=STATUS_CONCLUIDOS).count()

        # ✅ DateField → __range DIRETO (SEM __date)
        hoje = timezone.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)

        concluidas_semana = all_tarefas.filter(
            status__in=STATUS_CONCLUIDOS,
            concluida_em__range=[inicio_semana, fim_semana]  # ✅ CORRETO para DateField
        ).count()

        faltam = pendentes

        print(f"✅ SUCESSO: Semana {inicio_semana} a {fim_semana} = {concluidas_semana}")

        context.update({
            'pendentes': pendentes,
            'concluidas': concluidas,
            'concluidas_semana': concluidas_semana,
            'faltam': faltam,
            'inicio_semana': inicio_semana,
            'fim_semana': fim_semana,
        })

        return context


@method_decorator(login_required, name='dispatch')
class TarefaListOrdenadaView(ListView):
    """
    Página moderna de listagem de tarefas com múltiplas opções de ordenação.
    Ordenações disponíveis:
    - tarefa_n: Por número da tarefa
    - nome_interessado: Alfabética por nome do interessado
    - atualizado_em: Por data de atualização
    - fase_analise: Por fase da análise
    """
    model = tarefassamc
    template_name = 'tarefas/tarefa_list_moderna.html'
    context_object_name = 'tarefas'
    paginate_by = 20

    OPcoes_ORDENACAO = [
        ('tarefa_n', 'Número da Tarefa'),
        ('nome_interessado', 'Nome do Interessado (A-Z)'),
        ('-nome_interessado', 'Nome do Interessado (Z-A)'),
        ('-atualizado_em', 'Atualização (Mais Recentes)'),
        ('atualizado_em', 'Atualização (Mais Antigas)'),
        ('nome_tarefa__nome', 'Fase da Análise (A-Z)'),
        ('-nome_tarefa__nome', 'Fase da Análise (Z-A)'),
        ('-pk', 'Mais Recentes (ID)'),
        ('pk', 'Mais Antigas (ID)'),
    ]

    def get_queryset(self):
        queryset = tarefassamc.objects.filter(assigned_user=self.request.user).select_related('nome_tarefa')

        # Filtro de busca
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(nome_interessado__icontains=q) |
                Q(tarefa_n__icontains=q) |
                Q(nome_tarefa__nome__icontains=q) |
                Q(servico__icontains=q) |
                Q(status__icontains=q)
            )

        # Filtro por status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filtro por fase da análise
        fase = self.request.GET.get('fase')
        if fase:
            queryset = queryset.filter(nome_tarefa__id=fase)

        # Ordenação
        ordem = self.request.GET.get('ordem', '-atualizado_em')
        if ordem not in dict(self.OPcoes_ORDENACAO):
            ordem = '-atualizado_em'
        queryset = queryset.order_by(ordem)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        all_tarefas = tarefassamc.objects.filter(assigned_user=user)

        # Estatísticas
        STATUS_CONCLUIDOS = ['CONCLUIDA_INTERMEDIARIA', 'CONCLUIDA_FINALIZADA']
        pendentes = all_tarefas.exclude(status__in=STATUS_CONCLUIDOS).count()
        concluidas = all_tarefas.filter(status__in=STATUS_CONCLUIDOS).count()
        total = all_tarefas.count()

        hoje = timezone.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        concluidas_semana = all_tarefas.filter(
            status__in=STATUS_CONCLUIDOS,
            concluida_em__range=[inicio_semana, fim_semana]
        ).count()

        # Fases de análise para filtro
        fases_analise = tipo_servico.objects.all().order_by('nome')

        # Parâmetros atuais para manter na URL
        params = self.request.GET.copy()
        if 'page' in params:
            del params['page']

        context.update({
            'pendentes': pendentes,
            'concluidas': concluidas,
            'total': total,
            'concluidas_semana': concluidas_semana,
            'fases_analise': fases_analise,
            'opcoes_ordem': self.OPcoes_ORDENACAO,
            'ordem_atual': self.request.GET.get('ordem', '-atualizado_em'),
            'params': params,
            'STATUS_CONCLUIDOS': STATUS_CONCLUIDOS,
        })

        return context



@method_decorator(login_required, name='dispatch')
class TarefaDetailView(DetailView):
    model = tarefassamc
    template_name = 'tarefas/tarefa_detail.html'
    

@method_decorator(login_required, name='dispatch')
class TarefaCreateView(CreateView):
    model = tarefassamc
    form_class = TarefaForm
    template_name = 'tarefas/tarefa_form.html'
    success_url = reverse_lazy('tarefas:tarefa_list')

    def form_valid(self, form):
        form.instance.assigned_user = self.request.user
        
        # ✅ Mesma lógica
        STATUS_CONCLUIDOS = ['CONCLUIDA_INTERMEDIARIA', 'CONCLUIDA_FINALIZADA']
        if form.instance.status in STATUS_CONCLUIDOS and not form.instance.concluida_em:
            form.instance.concluida_em = timezone.now()
        
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TarefaUpdateView(UpdateView):
    model = tarefassamc
    form_class = TarefaForm
    template_name = 'tarefas/tarefa_form.html'
    success_url = reverse_lazy('tarefas:tarefa_list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.assigned_user = self.request.user
        
        # ✅ Preenche concluida_em
        STATUS_CONCLUIDOS = ['CONCLUIDA_INTERMEDIARIA', 'CONCLUIDA_FINALIZADA']
        if instance.status in STATUS_CONCLUIDOS and not instance.concluida_em:
            instance.concluida_em = timezone.now()
            print(f"✅ UPDATE: {instance.pk} concluida_em={instance.concluida_em}")
        
        instance.save()
        return super().form_valid(form)

    

@method_decorator(login_required, name='dispatch')
class TarefaDeleteView(DeleteView):
    model = tarefassamc
    template_name = 'tarefas/tarefa_confirm_delete.html'
    success_url = '/tarefas/'

@method_decorator(login_required, name='dispatch')
class GerarDocumentoView(DetailView):
    """
    View responsável por extrair dados da tarefa e aplicar nos templates 
    de documentos (ofícios, despachos, etc) do script aut_cobranca.py.
    """
    model = tarefassamc
    template_name = 'tarefas/exibir_documento.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        tipo_doc = kwargs.get('tipo', 'despacho')
        
        try:
            texto_gerado = gerar_texto_documento(self.object, tipo_doc)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'tipo': tipo_doc,
                    'conteudo': texto_gerado
                })

            context = self.get_context_data(
                object=self.object,  # necessário para usar object.pk no template
                texto_documento=texto_gerado,
                tipo_documento=tipo_doc.upper().replace('_', ' ')
            )
            return self.render_to_response(context)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
@method_decorator(login_required, name='dispatch')
class RelatorioPorUsuarioView(View):
    def get(self, request, *args, **kwargs):
        # Agrupa tarefas por usuário
        dados = tarefassamc.objects.values('assigned_user__username')\
            .annotate(total=Count('id'))\
            .order_by('-total')
        
        detalhes = tarefassamc.objects.filter(assigned_user=request.user).order_by('atualizado_em')

        context = {
            'titulo': 'Relatório de Tarefas por Usuário',
            'dados_agrupados': dados,
            'tarefas': detalhes,
            'data_geracao': timezone.now()
        }
        return render_to_pdf(request, 'tarefas/relatorio_pdf.html', context)
    
@method_decorator(login_required, name='dispatch')
class RelatorioConcluidasView(View):
    def get(self, request, *args, **kwargs):
        inicio = request.GET.get('inicio')
        fim = request.GET.get('fim')

        tarefas = tarefassamc.objects.filter(
            status__in=['CONCLUIDA_INTERMEDIARIA', 'CONCLUIDA_FINALIZADA'],
            assigned_user=request.user
        )

        if inicio and fim:
            try:
                from datetime import date
                tarefas = tarefas.filter(
                    concluida_em__range=[
                        date.fromisoformat(inicio),
                        date.fromisoformat(fim)
                    ]
                )
            except ValueError:
                messages.warning(request, 'Formato de data inválido. Use YYYY-MM-DD.')

        context = {
            'titulo': 'Relatório de Tarefas Concluídas',
            'tarefas': tarefas,
            'periodo': f"{inicio} a {fim}" if inicio else "Todo o período",
            'data_geracao': timezone.now()
        }
        return render_to_pdf(request, 'tarefas/relatorio_pdf.html', context)


@method_decorator(login_required, name='dispatch')
class ExportCSVView(View):
    def get(self, request, *args, **kwargs):
        # Exporta tarefas do usuário logado para CSV
        tarefas = tarefassamc.objects.filter(assigned_user=request.user)

        # Campos a exportar
        fieldnames = [
            'pk', 'nome_interessado', 'CPF', 'tarefa_n', 'tarefa_a', 'sei_n', 'procj',
            'servico', 'nome_tarefa', 'nome_serv', 'der_tarefa', 'valor', 'status', 'nb1',
            'historico', 'oficio1', 'oficio2', 'Competencia', 'data_irregular', 'assigned_user'
        ]

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for t in tarefas:
            # Acesso defensivo para evitar AttributeError se o modelo/BD estiver dessincronizado
            nb1_val = getattr(t, 'nb1', '')
            nome_tarefa = ''
            try:
                nome_tarefa = t.nome_tarefa.nome if getattr(t, 'nome_tarefa', None) else ''
            except Exception:
                nome_tarefa = ''

            nome_serv = ''
            try:
                nome_serv = t.nome_serv.nome if getattr(t, 'nome_serv', None) else ''
            except Exception:
                nome_serv = ''

            assigned_username = ''
            au = getattr(t, 'assigned_user', None)
            try:
                assigned_username = au.username if au else ''
            except Exception:
                assigned_username = ''

            writer.writerow({
                'pk': getattr(t, 'pk', ''),
                'nome_interessado': getattr(t, 'nome_interessado', ''),
                'CPF': getattr(t, 'CPF', ''),
                'tarefa_n': getattr(t, 'tarefa_n', ''),
                'tarefa_a': getattr(t, 'tarefa_a', ''),
                'sei_n': getattr(t, 'sei_n', ''),
                'procj': getattr(t, 'procj', ''),
                'servico': getattr(t, 'servico', ''),
                'nome_tarefa': nome_tarefa,
                'nome_serv': nome_serv,
                'der_tarefa': getattr(t, 'der_tarefa', ''),
                'valor': getattr(t, 'valor', ''),
                'status': getattr(t, 'status', ''),
                'nb1': nb1_val,
                'historico': getattr(t, 'historico', ''),
                'oficio1': getattr(t, 'oficio1').isoformat() if getattr(t, 'oficio1', None) else '',
                'oficio2': getattr(t, 'oficio2').isoformat() if getattr(t, 'oficio2', None) else '',
                'Competencia': getattr(t, 'Competencia').isoformat() if getattr(t, 'Competencia', None) else '',
                'data_irregular': getattr(t, 'data_irregular').isoformat() if getattr(t, 'data_irregular', None) else '',
                'assigned_user': assigned_username
            })

        resp = HttpResponse(output.getvalue(), content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename="tarefas_export.csv"'
        return resp


@method_decorator(login_required, name='dispatch')
class ImportCSVView(View):
    def post(self, request, *args, **kwargs):
        form = CSVUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, 'Arquivo inválido.')
            return redirect('tarefas:tarefa_list')

        csv_file = form.cleaned_data['csv_file']
        try:
            decoded = csv_file.read().decode('utf-8')
        except Exception:
            messages.error(request, 'Falha ao ler o arquivo. Use UTF-8.')
            return redirect('tarefas:tarefa_list')

        reader = csv.DictReader(io.StringIO(decoded))
        created = 0
        updated = 0
        errors = []
        row_num = 1
        for row in reader:
            # Tenta atualizar por pk se existir
            pk = row.get('pk') or ''
            obj = None
            if pk:
                try:
                    obj = tarefassamc.objects.get(pk=pk)
                except tarefassamc.DoesNotExist:
                    obj = None

            if not obj:
                obj = tarefassamc()

            # Mapear campos simples
            obj.nome_interessado = row.get('nome_interessado') or ''
            obj.CPF = row.get('CPF') or ''
            obj.tarefa_n = row.get('tarefa_n') or ''
            obj.tarefa_a = row.get('tarefa_a') or ''
            obj.sei_n = row.get('sei_n') or ''
            obj.procj = row.get('procj') or ''
            obj.servico = row.get('servico') or None
            obj.der_tarefa = row.get('der_tarefa') or ''
            obj.valor = row.get('valor') or ''
            obj.status = row.get('status') or ''
            obj.nb1 = row.get('nb1') or ''
            obj.historico = row.get('historico') or ''

            # Datas: tenta vários formatos (ISO, DD/MM/YYYY, DD-MM-YYYY, MM/DD/YYYY)
            def try_parse_date(val):
                if not val:
                    return None
                val = val.strip()
                # aceitar também valores já no formato YYYY-MM-DD
                from datetime import datetime
                formats = [
                    '%Y-%m-%d',
                    '%Y/%m/%d',
                    '%d/%m/%Y',
                    '%d-%m-%Y',
                    '%m/%d/%Y',
                ]
                for fmt in formats:
                    try:
                        return datetime.strptime(val, fmt).date()
                    except Exception:
                        continue
                # tentativa final: tentar interpretar apenas números YYYYMMDD
                if val.isdigit() and len(val) == 8:
                    try:
                        return datetime.strptime(val, '%Y%m%d').date()
                    except Exception:
                        pass
                return None

            for date_field in ('oficio1', 'oficio2', 'Competencia', 'data_irregular'):
                val = (row.get(date_field) or '').strip()
                parsed = try_parse_date(val)
                if parsed:
                    obj.__dict__[date_field] = parsed
                else:
                    obj.__dict__[date_field] = None
                    if val:
                        errors.append(f"Linha {row_num}: campo '{date_field}' formato inválido ('{val}')")

            # Foreign keys por nome
            nt = row.get('nome_tarefa') or ''
            if nt:
                obj.nome_tarefa = tipo_servico.objects.filter(nome=nt).first()
            else:
                obj.nome_tarefa = None

            ns = row.get('nome_serv') or ''
            if ns:
                obj.nome_serv = nome_motiv.objects.filter(nome=ns).first()
            else:
                obj.nome_serv = None

            # assigned_user por username
            au = row.get('assigned_user') or ''
            if au:
                obj.assigned_user = User.objects.filter(username=au).first()
            else:
                obj.assigned_user = request.user

            # Salva
            if obj.pk:
                obj.save()
                updated += 1
            else:
                obj.save()
                created += 1

            row_num += 1

        messages.success(request, f'Importação concluída: {created} criadas, {updated} atualizadas.')
        if errors:
            sample = errors[:5]
            messages.warning(request, f'Foram detectados {len(errors)} erros de formato de data. Exemplos: {"; ".join(sample)}')
        return redirect('tarefas:tarefa_list')

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'tarefas/dashboard.html'


@method_decorator(login_required, name='dispatch')
class DashboardDataView(View):
    def get(self, request):
        tarefas = tarefassamc.objects.filter(assigned_user=request.user).values(
            'id', 'tarefa_n', 'nome_interessado', 'servico',
            'status', 'atualizado_em', 'concluida_em'
        )
        return JsonResponse({'tarefas': list(tarefas)})


