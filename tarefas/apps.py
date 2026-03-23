from django.apps import AppConfig
from django.apps import AppConfig

class TarefasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tarefas'

    def ready(self):
        import tarefas.signals

class TarefasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tarefas'