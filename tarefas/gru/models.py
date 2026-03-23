"""
💾 MODELO OPCIONAL PARA ARMAZENAR GRUs CONSULTADAS
tarefas/gru/models.py - Use se quiser persistir dados

⚠️ IMPORTANTE:
Se adicionar este modelo, execute:
python manage.py makemigrations
python manage.py migrate
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class GRU(models.Model):
    """
    Modelo para armazenar dados de GRUs consultadas.
    
    ✅ Armazena:
    - Dados da GRU (número, valor, status)
    - Histórico de movimentações
    - Data de consulta
    - Usuário que consultou
    """
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('PARCIALMENTE_PAGO', 'Parcialmente Pago'),
        ('CANCELADO', 'Cancelado'),
        ('VENCIDO', 'Vencido'),
    ]
    
    # Dados da GRU
    numero = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        help_text="Número único da GRU (32 dígitos)"
    )
    
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Valor total da GRU"
    )
    
    valor_recolhido = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Valor já recolhido"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        db_index=True
    )
    
    # Datas
    data_vencimento = models.DateField(
        null=True,
        blank=True,
        help_text="Data até quando pode ser paga"
    )
    
    data_pagamento = models.DateField(
        null=True,
        blank=True,
        help_text="Data em que foi paga"
    )
    
    # Detalhes
    orgao_responsavel = models.CharField(
        max_length=255,
        blank=True,
        help_text="Órgão responsável pela arrecadação"
    )
    
    descricao_receita = models.TextField(
        blank=True,
        help_text="Descrição do motivo/tipo de receita"
    )
    
    # Rastreamento
    usuario_consulta = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grus_consultadas',
        help_text="Usuário que consultou esta GRU"
    )
    
    tarefa_relacionada = models.ForeignKey(
        'tarefas.tarefassamc',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grus',
        help_text="Tarefa SAACB associada"
    )
    
    # Timestamps
    data_consulta = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora da consulta"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        help_text="Última atualização dos dados"
    )
    
    # JSON para histórico (se usar)
    historico_json = models.JSONField(
        default=list,
        blank=True,
        help_text="Histórico de movimentações (JSON)"
    )
    
    class Meta:
        verbose_name = 'GRU'
        verbose_name_plural = 'GRUs'
        ordering = ['-data_consulta']
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['status']),
            models.Index(fields=['data_consulta']),
            models.Index(fields=['usuario_consulta']),
        ]
    
    def __str__(self):
        return f"GRU {self.numero} - {self.status}"
    
    def get_valor_faltante(self):
        """Retorna o valor que ainda falta recolher"""
        return self.valor - self.valor_recolhido
    
    def esta_vencida(self):
        """Verifica se a GRU está vencida"""
        from django.utils import timezone
        if self.data_vencimento:
            return timezone.now().date() > self.data_vencimento
        return False
    
    def atualizar_status(self):
        """Atualiza status baseado na data de vencimento"""
        if self.status == 'PENDENTE' and self.esta_vencida():
            self.status = 'VENCIDO'
            self.save(update_fields=['status'])
    
    def adicionar_movimentacao(self, tipo, descricao, data=None):
        """Adiciona uma movimentação ao histórico"""
        if data is None:
            data = timezone.now().isoformat()
        
        evento = {
            'data': data,
            'tipo': tipo,
            'descricao': descricao
        }
        
        self.historico_json.append(evento)
        self.save(update_fields=['historico_json'])


class ConsultaGRU(models.Model):
    """
    Modelo para rastrear cada consulta feita à API SISGRU.
    
    ✅ Armazena:
    - Quando foi consultada
    - Quem consultou
    - Se teve sucesso
    - Tempo de resposta
    - Erros
    """
    
    RESULTADO_CHOICES = [
        ('sucesso', 'Sucesso'),
        ('erro', 'Erro'),
        ('timeout', 'Timeout'),
        ('invalido', 'Número Inválido'),
    ]
    
    numero_gru = models.CharField(
        max_length=32,
        db_index=True,
        help_text="Número da GRU consultada"
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='consultas_gru',
        help_text="Usuário que realizou a consulta"
    )
    
    data_consulta = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora da consulta"
    )
    
    resultado = models.CharField(
        max_length=20,
        choices=RESULTADO_CHOICES,
        help_text="Resultado da consulta"
    )
    
    tempo_resposta = models.FloatField(
        null=True,
        blank=True,
        help_text="Tempo de resposta em segundos"
    )
    
    mensagem_erro = models.TextField(
        blank=True,
        help_text="Mensagem de erro, se houver"
    )
    
    endereco_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP do cliente"
    )
    
    gru = models.ForeignKey(
        GRU,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='consultas',
        help_text="GRU que foi consultada"
    )
    
    class Meta:
        verbose_name = 'Consulta GRU'
        verbose_name_plural = 'Consultas GRU'
        ordering = ['-data_consulta']
        indexes = [
            models.Index(fields=['numero_gru']),
            models.Index(fields=['usuario']),
            models.Index(fields=['data_consulta']),
        ]
    
    def __str__(self):
        return f"Consulta {self.numero_gru} - {self.resultado}"


class GRUDownload(models.Model):
    """
    Modelo para rastrear downloads de PDFs de GRU.
    
    ✅ Armazena:
    - PDF baixado
    - Quem baixou
    - Quando
    """
    
    gru = models.ForeignKey(
        GRU,
        on_delete=models.CASCADE,
        related_name='downloads'
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='downloads_gru'
    )
    
    data_download = models.DateTimeField(
        auto_now_add=True
    )
    
    arquivo = models.FileField(
        upload_to='gru_pdfs/%Y/%m/%d/',
        help_text="Arquivo PDF da GRU"
    )
    
    class Meta:
        verbose_name = 'Download GRU'
        verbose_name_plural = 'Downloads GRU'
        ordering = ['-data_download']
    
    def __str__(self):
        return f"Download {self.gru.numero} - {self.data_download}"


# ==================== ADMIN ===================

from django.contrib import admin

@admin.register(GRU)
class GRUAdmin(admin.ModelAdmin):
    list_display = ['numero', 'status', 'valor', 'valor_recolhido', 'data_vencimento', 'data_consulta']
    list_filter = ['status', 'data_consulta', 'data_vencimento']
    search_fields = ['numero', 'descricao_receita']
    readonly_fields = ['data_consulta', 'data_atualizacao']
    
    fieldsets = (
        ('Informações da GRU', {
            'fields': ['numero', 'valor', 'valor_recolhido', 'status']
        }),
        ('Datas', {
            'fields': ['data_vencimento', 'data_pagamento', 'data_consulta', 'data_atualizacao']
        }),
        ('Detalhes', {
            'fields': ['orgao_responsavel', 'descricao_receita']
        }),
        ('Rastreamento', {
            'fields': ['usuario_consulta', 'tarefa_relacionada'],
            'classes': ['collapse']
        }),
    )


@admin.register(ConsultaGRU)
class ConsultaGRUAdmin(admin.ModelAdmin):
    list_display = ['numero_gru', 'usuario', 'resultado', 'data_consulta', 'tempo_resposta']
    list_filter = ['resultado', 'data_consulta']
    search_fields = ['numero_gru', 'usuario__username']
    readonly_fields = ['data_consulta', 'endereco_ip']


@admin.register(GRUDownload)
class GRUDownloadAdmin(admin.ModelAdmin):
    list_display = ['gru', 'usuario', 'data_download']
    list_filter = ['data_download']
    search_fields = ['gru__numero', 'usuario__username']
    readonly_fields = ['data_download']
