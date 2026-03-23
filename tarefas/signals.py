# tarefas/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import tarefassamc

@receiver(pre_save, sender=tarefassamc)
def registrar_mudanca_status(sender, instance, **kwargs):
    if not instance.pk:
        return  # criação

    old = sender.objects.filter(pk=instance.pk).only('status', 'historico').first()
    if not old:
        return

    if instance.status != old.status:
        data_hora = timezone.now().strftime("%d/%m/%Y %H:%M")
        log_entry = f"[{data_hora}] Status alterado de '{old.status}' para '{instance.status}'.\n"

        instance.historico = (log_entry + (old.historico or ""))
