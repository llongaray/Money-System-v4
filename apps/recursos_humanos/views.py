from django.shortcuts import render, redirect
from .forms import FuncionarioForm
from .models import Funcionario
from apps.financeiro.models import Gasto, Conta
from apps.financeiro.forms import GastoForm, ContaForm
from decimal import Decimal
import holidays
from datetime import date

from openpyxl import Workbook
import csv
from django.http import HttpResponse

def funcionarios(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        #if form.is_valid():
        form.save()
        print("Savo!")
        return redirect('rh:formGastos')
    else:
        form = FuncionarioForm()
    
    funcionarios = Funcionario.objects.all()
    funcionarios_list = []
    
    for funcionario in funcionarios:
        funcionarios_list.append({
            'nome': funcionario.nome_completo,
            'cpf': funcionario.cpf,
            'tipo_contrato': funcionario.tipo_contrato,
            'cnpj': funcionario.cnpj,
            'salario': funcionario.salario,
            'empresa': funcionario.empresa,
            'status_atividade': funcionario.status_atividade,
        })
    
    return render(request, 'recursos_humanos/employee_actions.html', {
        'funcionarios': funcionarios_list,
        'form': form,
    })

def get_dias_uteis_mes_atual():
    # Obtendo os feriados nacionais do Brasil
    cal = holidays.Brazil()

    # Obtendo o mês e o ano atual
    today = date.today()
    year = today.year
    month = today.month

    # Contagem dos dias úteis
    dias_uteis = 0

    # Iterando sobre cada dia do mês atual
    for day in range(1, 32):
        try:
            # Verificando se o dia é útil (não é sábado, domingo ou feriado)
            current_date = date(year, month, day)
            if current_date.weekday() < 5 and current_date not in cal:
                dias_uteis += 1
        except ValueError:
            # Se houver um erro ao criar a data, significa que ultrapassamos o último dia do mês
            break

    return dias_uteis



def download_excel_model(request):
    # Cria um novo workbook
    wb = Workbook()
    ws = wb.active
    
    # Defina os cabeçalhos das colunas
    headers = [
        "Nome Completo", "Data de Nascimento", "CPF", "CNPJ", 
        "Tipo de Contrato", "Tempo de Contrato", "Salário", "Turno", 
        "Horário Diário", "VR Ativo", "VR Valor Diário", "VT Ativo", 
        "VT Valor Diário", "Setor", "Status de Atividade"
    ]
    
    # Adicione os cabeçalhos à primeira linha
    ws.append(headers)
    
    # Configura o nome do arquivo para download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="modelo_funcionarios.xlsx"'

    # Salva o workbook e o envia como resposta
    wb.save(response)
    
    return response

def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(decoded_file)

        for row in csv_reader:
            funcionario = Funcionario(
                nome_completo=row['Nome Completo'],
                data_nascimento=row['Data de Nascimento'],
                cpf=row['CPF'],
                cnpj=row['CNPJ'],
                tipo_contrato=row['Tipo de Contrato'],
                tempo_contrato=row['Tempo de Contrato'],
                salario=row['Salário'],
                turno=row['Turno'],
                horario_diario=row['Horário Diário'],
                vr_ativo=row['VR Ativo'],
                vr_valor_diario=row['VR Valor Diário'],
                vt_ativo=row['VT Ativo'],
                vt_valor_diario=row['VT Valor Diário'],
                setor=row['Setor'],
                status_atividade=row['Status de Atividade']
            )
            funcionario.save()

    return redirect('rh:tableFuncionarios')


def formGastos(request):
    conta_form = ContaForm()
    gasto_form = GastoForm()
    
    # Obtém todas as contas do banco de dados
    contas = Conta.objects.all()
    print("formGastos em uso...")
    if request.method == 'POST':  # Verifica se o formulário de Gasto foi submetido
        print("Recebendo POST Gasto")
        gasto_form = GastoForm(request.POST, request.FILES)
        if gasto_form.is_valid():
            print("Formulário de gasto válido")
            gasto = gasto_form.save(commit=False)
            # Obter a conta associada ao gasto
            conta_nome = request.POST.get('nome_associado')
            conta = Conta.objects.get(nome=conta_nome)
            # Obter os valores associados à conta selecionada
            vencimento = conta.vencimento_dia
            money_poa = conta.Money_POA
            money_sle = conta.Money_SLE
            money_sm = conta.Money_SM
            park_guaiba = conta.Park_Guaiba

            # Preencher os campos de vencimento e empresa com os valores associados à conta
            gasto.vencimento_dia = vencimento
            gasto.Money_POA = money_poa
            gasto.Money_SLE = money_sle
            gasto.Money_SM = money_sm
            gasto.Park_Guaiba = park_guaiba
            gasto.save()
            print("Gasto salvo com sucesso")
        else:
            print("Erros no formulário de gasto:", gasto_form.errors)
    
    context = {
        'conta_form': conta_form,
        'gasto_form': gasto_form,
        'contas': contas,  # Envia as contas para o template
    }
    return render(request, 'recursos_humanos/form_gastos.html', context)
