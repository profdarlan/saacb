# Generated migration - Integração SAACB ↔ Planilha Cálculos

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0014_alter_tarefassamc_concluida_em'),  # Última migration existente
    ]

    operations = [
        migrations.AddField(
            model_name='tarefassamc',
            name='valor_original_calculado',
            field=models.DecimalField(
                max_digits=12,
                decimal_places=2,
                null=True,
                blank=True,
                verbose_name="Valor Original Calculado"
            ),
        ),
        migrations.AddField(
            model_name='tarefassamc',
            name='valor_corrigido_calculado',
            field=models.DecimalField(
                max_digits=12,
                decimal_places=2,
                null=True,
                blank=True,
                verbose_name="Valor Corrigido Calculado"
            ),
        ),
        migrations.AddField(
            model_name='tarefassamc',
            name='valor_diferenca',
            field=models.DecimalField(
                max_digits=12,
                decimal_places=2,
                null=True,
                blank=True,
                verbose_name="Diferença Calculada"
            ),
        ),
        migrations.AddField(
            model_name='tarefassamc',
            name='detalhes_calculo',
            field=models.JSONField(
                null=True,
                blank=True,
                verbose_name="Detalhes do Cálculo"
            ),
        ),
        migrations.AddField(
            model_name='tarefassamc',
            name='relatorio_pdf',
            field=models.FileField(
                upload_to='relatorios_calculos/',
                null=True,
                blank=True,
                verbose_name="Relatório PDF"
            ),
        ),
        migrations.AddField(
            model_name='tarefassamc',
            name='calculado_em',
            field=models.DateTimeField(
                null=True,
                blank=True,
                verbose_name="Calculado em"
            ),
        ),
    ]
