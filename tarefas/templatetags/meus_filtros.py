# tarefas/templatetags/meus_filtros.py
from django import template

register = template.Library()

@register.filter
def get_label(obj, field_name):
    """Retorna o verbose_name do campo do modelo"""
    try:
        return obj._meta.get_field(field_name).verbose_name
    except Exception:
        return field_name.replace('_', ' ').capitalize()
