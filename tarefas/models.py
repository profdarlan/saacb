from django.db import models
from django.contrib.auth.models import User
import django.dispatch
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class tipo_servico(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class nome_motiv(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class conc_analise(models.Model):
    conc = models.CharField(max_length=100)
    conc_exp = models.TextField(blank=True, null=True)
    fim = models.CharField('',choices=(
        ('PROCEDENTE', 'PROCEDENTE'),
        ('PARCIALMENTE PROCEDENTE', 'PARCIALMENTE PROCEDENTE'),
        ('IMPROCEDENTE', 'IMPROCEDENTE'),
        ),
        max_length=100, blank=True, null=True)

    def __str__(self):
        return self.conc
    
class tarefassamc(models.Model):
    nome_interessado = models.CharField('Nome', max_length=100, blank=True, null=True)
    CPF = models.CharField("CPF", max_length=20, blank=True, null=True)
    tarefa_n = models.CharField('Tarefa Principal', max_length=50, blank=True, null=True)
    tarefa_a = models.CharField('Tarefa Anterior', max_length=50, blank=True, null=True)
    sei_n = models.CharField('Número SEI', max_length=50, blank=True, null=True)
    procj = models.CharField('Número do Processo Judicial', max_length=50, blank=True, null=True)
    servico = models.CharField("Serviço", choices=(
        ('ANALISE', "ANALISE"),
        ('ANALISE cobranca', "ANALISE - Cobrança"),
        ('ANALISE exigencia', "ANALISE - Exigência"),
        ('ANALISE corregedoria', "ANALISE - Corregedoria"),
        ('ANALISE pendencia', "ANALISE - Pendência"),
        ('ANALISE Concluir', "ANALISE - Concluir"),
        ('ANALISE recurso', "ANALISE - Recurso"),
        ('ANALISE judicial', "ANALISE - Judicial"),
        ('CONCLUIDO', "CONCLUIDO"),
        ('CONCLUIDO pendente', "CONCLUIDO - pendente"),
        ('PA', "PA - Aguardando Processo"),
        ('PARECER SOCIAL', "PARECER SOCIAL - Aguardando Parecer Social"),
        ('PERICIA', "PERICIA - Aguardando Perícia Médica"),
        ('PROCURADORIA', "PROCURADORIA - Aguardando Procuradoria"),
    ),
        max_length=100, null=True
    )
    nome_tarefa = models.ForeignKey(tipo_servico, verbose_name="Fase da Análise", on_delete=models.CASCADE, blank=True, null=True)
    nome_serv = models.ForeignKey(nome_motiv, verbose_name="Motivo do Ressarcimento", on_delete=models.CASCADE, max_length=100, blank=True, null=True)
    der_tarefa = models.CharField("DER Tarefa", max_length=20, blank=True, null=True)
    data_def = models.CharField("Data da ciência - ofício defesa", max_length=20, blank=True, null=True)
    data_rec = models.CharField("Data da ciência - ofício recurso", max_length=20, blank=True, null=True)
    nb1 = models.CharField("Benefício 1", max_length=20, blank=True, null=True)
    nb2 = models.CharField("Benefício 2", max_length=20, blank=True, null=True)
    sit_ben = models.CharField("Situação do Benefício", max_length=100, blank=True, null=True)
    aps = models.CharField("APS Manutenção", max_length=100, blank = True, null = True)
    prazo = models.CharField("Prazo Defesa", choices=(
        ('30 dias', "30 dias"),
        ('60 dias', "60 dias"),
    ),
        max_length=100, blank=True, null=True
    )
    defesa_ap = models.CharField("Apresentou defesa?", choices=(
        ('sim', "Sim"),
        ('nao', "Não"),
    ),
        max_length=100, blank=True, null=True
    )
    categoria = models.CharField("Categoria da irregularidade", max_length=100, blank=True, null=True)
    tip_con = models.CharField("Tipo de Crédito Devido", choices=(
        ('Crédito', "Crédito"),
        ('Dano ao Erário', "Dano ao Erário"),
    ),
        max_length=100, blank=True, null=True
    )
    
    oficio1 = models.DateField("Ofício Defesa - ciência", max_length=20, blank=True, null=True)
    AR1 = models.CharField("Aviso de Recebimento e documentos - Qual o tipo do comprovante?",choices=(
        ('AR Digital', "AR Digital"),
        ('Edital', "Edital"),
        ('Atestado Pessoal', "Atestado Pessoal"),
        ('Acesso à tarefa eletrônica de cobrança administrativa', "Acesso à tarefa eletrônica de cobrança administrativa"),
    ),
         max_length=100, blank=True, null=True)
    oficio2 = models.DateField("Ofício Recurso - ciência", max_length=20, blank=True, null=True)
    AR2 = models.TextField("Aviso de Recebimento e documentos - Qual o tipo do comprovante?",choices=(
        ('AR Digital', "AR Digital"),
        ('Edital', "Edital"),
        ('Atestado Pessoal', "Atestado Pessoal"),
        ('Acesso à tarefa eletrônica de cobrança administrativa', "Acesso à tarefa eletrônica de cobrança administrativa"),
    ),
                           blank=True, null=True)
    Competencia = models.DateField("Competência", blank=True, null=True)
    data_irregular = models.DateField("Data de início da irregularidade", blank=True, null=True)
    Periodo_irregular = models.TextField("Periodo irregular", blank=True, null=True)
    valor = models.CharField("Valor do débito", max_length=20, blank = True, null = True)
    obs1 = models.TextField("Relatório - faça um breve resumo da defesa:", blank=True, null=True)
    es_conc = models.ForeignKey(conc_analise, verbose_name="Conclusão da Análise", on_delete=models.CASCADE, blank=True, null=True)
    obs2 = models.TextField("Direito e conclusão - vai aparecer antes da conclusão", blank=True, null=True)
    resp_credito = models.CharField("Quem é o responsável pelo crédito?", choices=(
        ('1', "Titular do benefício"),
        ('2', "Responsável Legal"),
    ),
        max_length=100, blank = True, null = True
        )
    responsavel = models.CharField("Responsável Legal", max_length=100, blank = True, null = True)
    CPF_R = models.CharField("CPF Responsável", max_length=20, blank=True, null=True)
    Conclusao = models.CharField("Conclusão", choices=(
        ('REGULAR', "REGULAR"),
        ('IRREGULAR Boa fé', "IRREGULAR - Boa fé"),
        ('IRREGULAR Má fé', "IRREGULAR - Má fé"),
        ('PARCIALMENTE IRREGULAR', "PARCIALMENTE IRREGULAR"),
    ),  max_length=100, blank=True, null=True)
    status = models.CharField("Status", choices=(
        ('PENDENTE', "PENDENTE"),
        ('PENDENTE', "PENDENTE - CORREÇÃO"),
        ('CONCLUIDA_INTERMEDIARIA', "CONCLUÍDA - INTERMEDIÁRIA"),
        ('CONCLUIDA_FINALIZADA', "CONCLUÍDA - FINALIZADA")
    ), max_length=100, blank=True, null=True)
    historico = models.TextField("Histórico(Fundamento da cobrança)", blank=True, null=True)
    env_serv = models.CharField("Envolvimento de Servidor? Informe Situação Atual", choices=(
        ('Servidor Ativo', "Servidor Ativo"),
        ('Servidor Inativo - demitido/aposentado', "Servidor Inativo - demitido/aposentado"),
        ('Pensionista', "Pensionista"),
        ('Não Envolvido', "Não Envolvido"),
    ), max_length=50, blank=True, null=True)
    servidor = models.CharField("Matrícula Servidor Responsável", max_length=100, blank = True, null = True)
    concluida_em = models.DateField(blank=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    assigned_user = models.ForeignKey(User, verbose_name="Usuário Responsável", on_delete=models.SET_NULL, blank=True, null=True)

    # Campos de integração com calculadora de créditos (planilha_saacb)
    valor_original_calculado = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name="Valor Original Calculado"
    )
    valor_corrigido_calculado = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name="Valor Corrigido Calculado"
    )
    valor_diferenca = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name="Diferença Calculada"
    )
    detalhes_calculo = models.JSONField(
        null=True, blank=True,
        verbose_name="Detalhes do Cálculo"
    )
    relatorio_pdf = models.FileField(
        upload_to='relatorios_calculos/', null=True, blank=True,
        verbose_name="Relatório PDF"
    )
    calculado_em = models.DateTimeField(
        null=True, blank=True,
        verbose_name="Calculado em"
    )

    # Campo para rastrear aprovação dos cálculos
    calculos_aprovados = models.BooleanField(
        default=False,
        verbose_name="Cálculos Aprovados (migrar para Valor)"
    )


class GRU(models.Model):
    """Modelo para armazenar GRUs geradas/consultadas pelo sistema."""
    STATUS_CHOICES = (
        ('PENDENTE', 'PENDENTE'),
        ('PAGA', 'PAGA'),
        ('VENCIDA', 'VENCIDA'),
        ('CANCELADA', 'CANCELADA'),
    )

    beneficiario_nome = models.CharField(max_length=200, blank=True, null=True)
    beneficiario_cpf = models.CharField(max_length=30, blank=True, null=True)
    codigo_recolhimento = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    competencia = models.DateField(blank=True, null=True)
    vencimento = models.DateField(blank=True, null=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    pdf_file = models.FileField(upload_to='gru_pdfs/', blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='grus_criadas')
    criado_em = models.DateTimeField(auto_now_add=True)
    concluida_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'GRU'
        verbose_name_plural = 'GRUs'

    def __str__(self):
        return f"GRU {self.codigo_recolhimento or self.id} - {self.beneficiario_nome or ''}"





# Signal para migrar valores calculados aprovados para o campo valor
@receiver(pre_save, sender=tarefassamc)
def migrar_valores_aprovados(sender, instance, **kwargs):
    """
    Quando os cálculos são aprovados (checkbox marcado), 
    migre os valores calculados para o campo valor principal
    e atualiza o status para indicar que foi migrado.
    """
    # Só migrar se o cálculo foi aprovado
    if not instance.calculos_aprovados:
        return
    
    # Só migrar se houver valores calculados
    if (instance.valor_original_calculado is None or 
        instance.valor_corrigido_calculado is None or 
        instance.valor_diferenca is None):
        return
    
    # Migrar valores calculados para o campo valor principal
    if instance.valor_original_calculado:
        instance.valor = instance.valor_original_calculado
    if instance.valor_corrigido_calculado:
        instance.valor = instance.valor_corrigido_calculado
    
    # Atualizar status para indicar que foi migrado
    # Se o status for PENDENTE, muda para PENDENTE - MIGRADO
    # Isso mostra que os cálculos foram aprovados mas ainda não finalizados
    if instance.status == 'PENDENTE':
        instance.status = 'PENDENTE - MIGRADO'
