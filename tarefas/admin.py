from django.contrib import admin, messages
from django import forms
from django.template.response import TemplateResponse
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.auth.models import User
from .models import tarefassamc, tipo_servico, Role, UserProfile, nome_motiv, conc_analise, GRU


class AssignUserActionForm(forms.Form):
	_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
	assigned_user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Usuário a atribuir')


class TarefassamcAdmin(admin.ModelAdmin):
	list_display = ('id', 'tarefa_n', 'nome_interessado','status', 'safe_assigned_user')
	search_fields = ('tarefa_n', 'nome_interessado')
	list_filter = ('status', 'servico','assigned_user')
	actions = ['assign_user']

	def assign_user(self, request, queryset):
		# Se o formulário ainda não foi submetido (flag 'apply'), exibe página de confirmação
		if 'apply' not in request.POST:
			form = AssignUserActionForm(initial={
				'_selected_action': request.POST.getlist(ACTION_CHECKBOX_NAME)
			})
			context = {
				**self.admin_site.each_context(request),
				'title': 'Atribuir usuário às tarefas selecionadas',
				'queryset': queryset,
				'form': form,
				'opts': self.model._meta,
				'action_checkbox_name': ACTION_CHECKBOX_NAME,
			}
			return TemplateResponse(request, 'admin/tarefas/assign_user.html', context)

		user_pk = request.POST.get('assigned_user')
		if not user_pk:
			self.message_user(request, 'Nenhum usuário selecionado.', level=messages.WARNING)
			return
		try:
			user = User.objects.get(pk=user_pk)
		except User.DoesNotExist:
			self.message_user(request, 'Usuário inválido.', level=messages.ERROR)
			return
		updated = queryset.update(assigned_user=user)
		self.message_user(request, f'{updated} tarefas atualizadas para {user.username}.')
	assign_user.short_description = 'Atribuir usuário selecionado às tarefas'

	def safe_assigned_user(self, obj):
		try:
			au = getattr(obj, 'assigned_user', None)
			return au.username if au else ''
		except Exception:
			return ''

	safe_assigned_user.short_description = 'Usuário Responsável'

admin.site.site_header = "SAACB - Admin"
admin.site.site_title = "SAACB - Administração"
admin.site.index_title = "Seção de Apuração e Cobrança Administrativa de Benefícios"
admin.site.register(tarefassamc, TarefassamcAdmin)
admin.site.register(tipo_servico)
admin.site.register(nome_motiv)
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(conc_analise)
admin.site.register(GRU)
