"""
📝 FORMULÁRIOS PARA GERAÇÃO DE GRU
Módulo forms.py - Adicione ao seu projeto
"""

from django import forms
from django.core.exceptions import ValidationError
from .gru_service import SISGRUService, SISGRUAPIError, formatar_numero_gru
from tarefas.models import GRU
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class ConsultarGRUForm(forms.Form):
    """
    Formulário para consultar uma GRU na API SISGRU.
    
    ✅ Validações:
    - Formato do número (32 dígitos)
    - Conectividade com API
    - Credenciais
    """
    
    numero_gru = forms.CharField(
        label="Número da GRU",
        max_length=40,  # Permite formatação
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1000.0000.0001.2345.6789.0000.0000.00',
            'autocomplete': 'off',
            'pattern': '[0-9.-]{32,}',
        }),
        help_text="Digite ou cole o número da GRU (com ou sem formatação)"
    )
    
    usuario_sisgru = forms.CharField(
        label="Usuário Conecta.Gov.BR",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'autocomplete': 'off',
        }),
        help_text="Usuário registrado no Conecta.Gov.BR"
    )
    
    senha_sisgru = forms.CharField(
        label="Senha Conecta.Gov.BR",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
        }),
        help_text="Senha do seu usuário no Conecta.Gov.BR"
    )
    
    usar_producao = forms.BooleanField(
        label="Usar ambiente de PRODUÇÃO",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        help_text="Desmarque para usar HOMOLOGAÇÃO (recomendado para testes)"
    )
    
    gerar_pdf = forms.BooleanField(
        label="Gerar PDF automaticamente",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        help_text="Se marcado, gera PDF após consultar GRU"
    )
    
    def clean_numero_gru(self):
        """Valida e limpa o número da GRU"""
        numero = self.cleaned_data.get('numero_gru', '')
        
        if not numero:
            raise ValidationError('Número da GRU é obrigatório')
        
        # Remove formatação (pontos e hífens)
        numero_limpo = numero.replace('.', '').replace('-', '').replace(' ', '')
        
        # Valida comprimento
        if len(numero_limpo) != 32:
            raise ValidationError(
                f'Número da GRU deve ter 32 dígitos. Você digitou {len(numero_limpo)}.'
            )
        
        # Valida se são apenas dígitos
        if not numero_limpo.isdigit():
            raise ValidationError('Número da GRU deve conter apenas dígitos')
        
        # Retorna sem formatação para processamento
        return numero_limpo
    
    def clean_usuario_sisgru(self):
        """Valida usuário"""
        usuario = self.cleaned_data.get('usuario_sisgru', '').strip()
        
        if not usuario:
            raise ValidationError('Usuário é obrigatório')
        
        if len(usuario) < 3:
            raise ValidationError('Usuário muito curto')
        
        return usuario
    
    def clean_senha_sisgru(self):
        """Valida senha"""
        senha = self.cleaned_data.get('senha_sisgru', '')
        
        if not senha:
            raise ValidationError('Senha é obrigatória')
        
        if len(senha) < 6:
            raise ValidationError('Senha deve ter pelo menos 6 caracteres')
        
        return senha
    
    def clean(self):
        """Validação global do formulário"""
        cleaned_data = super().clean()
        
        # Tentar conectar à API
        try:
            usuario = cleaned_data.get('usuario_sisgru')
            senha = cleaned_data.get('senha_sisgru')
            usar_producao = cleaned_data.get('usar_producao', False)
            
            if usuario and senha:
                logger.info(f"Testando conexão com API SISGRU para {usuario}")
                
                service = SISGRUService(
                    usuario=usuario,
                    senha=senha,
                    producao=usar_producao
                )
                
                # Verificar disponibilidade
                if not service.verificar_disponibilidade():
                    raise ValidationError(
                        'API SISGRU indisponível. Tente novamente mais tarde. '
                        '(Disponível seg-sex 08:00-22:00, horário Brasília)'
                    )
                
        except SISGRUAPIError as e:
            raise ValidationError(f'Erro ao validar credenciais: {str(e)}')
        except Exception as e:
            logger.error(f"Erro na validação do formulário: {str(e)}")
            # Não bloqueia o formulário, deixa tentar na view
        
        return cleaned_data


class GerarGRUForm(forms.Form):
    """
    Formulário para gerar uma nova GRU.
    
    ⚠️ Nota: Esta é uma funcionalidade avançada que requer
    permissões especiais no Conecta.Gov.BR
    """
    
    valor = forms.DecimalField(
        label="Valor (em reais)",
        max_digits=12,
        decimal_places=2,
        required=True,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1000.00',
            'step': '0.01',
        }),
        help_text="Valor a ser recolhido"
    )
    
    data_vencimento = forms.DateField(
        label="Data de Vencimento",
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
        help_text="Até quando a GRU pode ser paga"
    )
    
    orgao_responsavel = forms.CharField(
        label="Órgão Responsável",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Secretaria de Estado de Fazenda',
        }),
        help_text="Órgão que irá recolher o valor"
    )
    
    descricao_receita = forms.CharField(
        label="Descrição da Receita",
        max_length=255,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ex: Multa administrativa por irregularidade em benefício',
        }),
        help_text="Motivo/descrição do recolhimento"
    )
    
    usuario_sisgru = forms.CharField(
        label="Usuário Conecta.Gov.BR",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    senha_sisgru = forms.CharField(
        label="Senha Conecta.Gov.BR",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        })
    )
    
    def clean_valor(self):
        """Valida valor"""
        valor = self.cleaned_data.get('valor')
        
        if valor and valor <= 0:
            raise ValidationError('Valor deve ser maior que zero')
        
        if valor and valor > 999999999.99:
            raise ValidationError('Valor muito alto')
        
        return valor
    
    def clean_data_vencimento(self):
        """Valida data de vencimento"""
        from datetime import date
        
        data = self.cleaned_data.get('data_vencimento')
        
        if data and data < date.today():
            raise ValidationError('Data de vencimento não pode ser no passado')
        
        return data


class GRUModelForm(forms.ModelForm):
    """ModelForm para criação/persistência de GRU no sistema."""

    class Meta:
        model = GRU
        fields = [
            'beneficiario_nome', 'beneficiario_cpf', 'codigo_recolhimento',
            'competencia', 'vencimento', 'valor', 'descricao'
        ]

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor and valor <= 0:
            raise ValidationError('Valor deve ser maior que zero')
        return valor


class FiltroGRUForm(forms.Form):
    """Formulário para filtrar GRUs já consultadas"""
    
    STATUS_CHOICES = [
        ('', 'Todos os status'),
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('PARCIALMENTE_PAGO', 'Parcialmente Pago'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    numero_gru = forms.CharField(
        label="Número GRU",
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite parte do número...',
        })
    )
    
    status = forms.ChoiceField(
        label="Status",
        choices=STATUS_CHOICES,
        required=False,
        initial='',
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    data_inicio = forms.DateField(
        label="Data de Início",
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
    )
    
    data_fim = forms.DateField(
        label="Data de Fim",
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
    )
    
    valor_minimo = forms.DecimalField(
        label="Valor Mínimo",
        max_digits=12,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
        })
    )
    
    valor_maximo = forms.DecimalField(
        label="Valor Máximo",
        max_digits=12,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '999999.99',
        })
    )
    
    def clean(self):
        """Valida filtros"""
        cleaned_data = super().clean()
        
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        
        if data_inicio and data_fim and data_inicio > data_fim:
            raise ValidationError('Data de início deve ser anterior à data de fim')
        
        valor_minimo = cleaned_data.get('valor_minimo')
        valor_maximo = cleaned_data.get('valor_maximo')
        
        if valor_minimo and valor_maximo and valor_minimo > valor_maximo:
            raise ValidationError('Valor mínimo deve ser menor que valor máximo')
        
        return cleaned_data
