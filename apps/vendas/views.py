from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal, InvalidOperation
import pandas as pd
from .models import BaseClientes, ExtDebitos

EXPECTED_COLUMNS = ["cliente_banco","cliente_cod_orgao","cliente_orgao","cliente_matricula","cliente_upag","cliente_uf","cliente_nome","cliente_cpf","cliente_valor","cliente_margem","cliente_margem_cartao","cliente_prazo","cliente_situacao"]

def handle_uploaded_file(f):
    if f.name.endswith('.csv'):
        df = pd.read_csv(f)
    elif f.name.endswith('.xls') or f.name.endswith('.xlsx') or f.name.endswith('.xlsb'):
        df = pd.read_excel(f)
    else:
        raise ValueError("Unsupported file format")
    return df

def import_clients(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return render(request, 'vendas/import_clients.html', {
                'error': 'Nenhum arquivo enviado.'
            })

        try:
            df = handle_uploaded_file(uploaded_file)
        except ValueError as e:
            return render(request, 'vendas/import_clients.html', {
                'error': str(e)
            })

        if list(df.columns) != EXPECTED_COLUMNS:
            return render(request, 'vendas/import_clients.html', {
                'error': 'Arquivo não segue o modelo de cabeçalho por favor reorganize para: ' + str(EXPECTED_COLUMNS)
            })

        for _, row in df.iterrows():
            cpf = row['cliente_cpf']
            cliente, created = BaseClientes.objects.get_or_create(
                cpf=cpf,
                defaults={'nome': row['cliente_nome'], 'uf': row['cliente_uf']}
            )

            if not created:
                cliente.nome = row['cliente_nome']
                cliente.uf = row['cliente_uf']
                cliente.save()

            try:
                cliente_valor = float(row['cliente_valor'])
                cliente_margem = float(row['cliente_margem'])
                cliente_margem_cartao = float(row['cliente_margem_cartao'])
                cliente_prazo = int(row['cliente_prazo'])
            except (ValueError, InvalidOperation):
                return render(request, 'vendas/import_clients.html', {
                    'error': 'Erro ao converter valores.'
                })

            debito, created = ExtDebitos.objects.get_or_create(
                id_cliente=cliente,
                banco=row['cliente_banco'],
                cod_orgao=row['cliente_cod_orgao'],
                orgao=row['cliente_orgao'],
                matricula=row['cliente_matricula'],
                upag=row['cliente_upag'],
                valor=cliente_valor,
                margem=cliente_margem,
                margem_cartao=cliente_margem_cartao,
                prazo=cliente_prazo,
                situacao=row['cliente_situacao']
            )
            if not created:
                debito.save()

        return render(request, 'vendas/import_clients.html', {
            'success': 'Dados importados com sucesso!'
        })

    return render(request, 'vendas/import_clients.html')

def siape_consulta(request):
    clientes = BaseClientes.objects.all()

    if 'cpf_filter' in request.GET:
        cpf_filter = request.GET['cpf_filter']
        if cpf_filter:
            clientes = clientes.filter(cpf=cpf_filter)

    return render(request, 'vendas/siape/consulta_de_clientes.html', {'clientes': clientes})

def cliente_detalhe(request, cliente_id):
    cliente = get_object_or_404(BaseClientes, pk=cliente_id)
    debitos = ExtDebitos.objects.filter(id_cliente=cliente)

    return render(request, 'vendas/siape/cliente_detalhe.html', {'cliente': cliente, 'debitos': debitos})