from django.contrib import admin
from .models import Conta, Gasto, Comprovante

class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'vencimento_dia', 'tipo_conta', 'data_cadastro')
    list_filter = ('tipo_conta', 'data_cadastro')
    search_fields = ('nome',)
    readonly_fields = ('data_cadastro',)

admin.site.register(Conta, ContaAdmin)

class GastoAdmin(admin.ModelAdmin):
    list_display = ('nome_associado', 'valor', 'vencimento_dia', 'status', 'data_cadastro')
    list_filter = ('status', 'data_cadastro')
    search_fields = ('nome_associado',)
    readonly_fields = ('data_cadastro',)

admin.site.register(Gasto, GastoAdmin)

class ComprovanteAdmin(admin.ModelAdmin):
    list_display = ('nome_associado', 'valor', 'vencimento_dia', 'status', 'data_cadastro')
    list_filter = ('status', 'data_cadastro')
    search_fields = ('nome_associado',)
    readonly_fields = ('data_cadastro',)

admin.site.register(Comprovante, ComprovanteAdmin)
