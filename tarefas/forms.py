from django import forms
from .models import tarefassamc

class TarefaForm(forms.ModelForm):
    class Meta:
        model = tarefassamc
        fields = '__all__'
        widgets = {
            'nome_interessado': forms.TextInput(attrs={'class': 'form-control'}),
            'CPF': forms.TextInput(attrs={'class': 'form-control'}),
            'tarefa_n': forms.TextInput(attrs={'class': 'form-control'}),
            'tarefa_a': forms.TextInput(attrs={'class': 'form-control'}),
            'sei_n': forms.TextInput(attrs={'class': 'form-control'}),
            'procj': forms.TextInput(attrs={'class': 'form-control'}),
            'servico': forms.Select(attrs={'class': 'form-select'}),
            'nome_tarefa': forms.Select(attrs={'class': 'form-select'}),
            'nome_serv': forms.Select(attrs={'class': 'form-select'}),
            'der_tarefa': forms.TextInput(attrs={'class': 'form-control'}),
            'data_ci': forms.TextInput(attrs={'class': 'form-control'}),
            'nb1': forms.TextInput(attrs={'class': 'form-control'}),
            'nb2': forms.TextInput(attrs={'class': 'form-control'}),
            'sit_ben': forms.TextInput(attrs={'class': 'form-control'}),
            'aps': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo': forms.Select(attrs={'class': 'form-select'}),
            'defesa_ap': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'tip_con': forms.Select(attrs={'class': 'form-select'}),
            'oficio1': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'AR1': forms.Select(attrs={'class': 'form-control', 'rows': 3}),
            'oficio2': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'AR2': forms.Select(attrs={'class': 'form-control', 'rows': 3}),
            'Competencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_irregular': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'Periodo_irregular': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'es_conc': forms.Select(attrs={'class': 'form-select'}),
            'obs1': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'obs2': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resp_credito': forms.Select(attrs={'class': 'form-select'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'CPF_R': forms.TextInput(attrs={'class': 'form-control'}),
            'Conclusao': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-control', 'rows': 3}),
            'historico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'env_serv': forms.Select(attrs={'class': 'form-select'}),
            'servidor': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_user': forms.Select(attrs={'class': 'form-select'}),
        }


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Arquivo CSV', help_text='Envie um arquivo .csv para importar tarefas')