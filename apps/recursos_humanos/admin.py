from django.contrib import admin
from .models import Funcionario
from .models import get_tipo_contrato_choices, get_setor_choices, get_empresas_choices, get_status_atividade_choices

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_completo', 'status_atividade')  # Define quais campos serão exibidos na lista de funcionários

# Registra o modelo Funcionario no admin
admin.site.register(Funcionario, FuncionarioAdmin)
