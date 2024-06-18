from django.urls import path
from .views import formContas, tableGastos, PDFView, EnviarComprovanteView

app_name = "financeiro"

urlpatterns = [
    path('financeiro/contas/', formContas, name="formContas"),
    path('financeiro/gastos/', tableGastos, name="tableGastos"),
    path('visualizar-gasto/<int:gasto_id>/', PDFView.as_view(), name='visualizar_gasto'),
    path('enviar-comprovante/', EnviarComprovanteView.as_view(), name='enviar_comprovante'),
]
