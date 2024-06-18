from django.urls import path
from .views import import_clients, siape_consulta, cliente_detalhe

app_name = "vendas"

urlpatterns = [
    path('import_clients/', import_clients, name="import_clients"),
    path('siape/consulta_de_clientes', siape_consulta, name="siape_consulta"),
    path('cliente/<int:cliente_id>/', cliente_detalhe, name='cliente_detalhe')
]
