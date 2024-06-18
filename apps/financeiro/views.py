# Definindo a função get_choice_id fora das views
def get_choice_id(choice):
    return choice.replace(" ", "_")

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import ContaForm, GastoForm, ComprovanteForm
from .models import Conta, Gasto, Comprovante
from datetime import datetime, date
import calendar
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.views import View
from django.views import generic

class PDFView(generic.TemplateView):
    model = Gasto
    template_name = "apps/financeiro/extra/visualizar_gasto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gasto_id = self.kwargs.get('gasto_id')
        gasto = get_object_or_404(Gasto, id=gasto_id)

        form = ComprovanteForm(initial={
            'gasto_id': gasto_id,
            'nome_associado': gasto.nome_associado,
            'valor': gasto.valor,
            'vencimento_dia': gasto.vencimento_dia,
            'status': gasto.status,
        })
        context['gasto'] = gasto
        context['form'] = form
        return context

class EnviarComprovanteView(View):
    def post(self, request, *args, **kwargs):
        form = ComprovanteForm(request.POST, request.FILES)
        if form.is_valid():
            gasto_id = request.POST.get('gasto_id')
            nome_associado = request.POST.get('nome_associado')
            valor = request.POST.get('valor')
            vencimento_dia = request.POST.get('vencimento_dia')
            status = request.POST.get('status')

            gasto = Gasto.objects.get(id=gasto_id)  # Obter o objeto Gasto
            gasto.status = status  # Atualizar o campo 'Status'
            gasto.save()  # Salvar as alterações

            comprovante = form.save(commit=False)
            comprovante.id_gasto = gasto_id
            comprovante.nome_associado = nome_associado
            comprovante.valor = valor
            comprovante.vencimento_dia = vencimento_dia
            comprovante.status = status
            comprovante.year_month = gasto.year_month
            comprovante.save()

            return redirect('financeiro:tableGastos')  # Redirecionar para a página de sucesso

        # Se o formulário não for válido, retorne uma resposta de erro 400
        return HttpResponseBadRequest("Formulário inválido")

def tableGastos(request):
    dados_relatorio = []

    # Obter o ano e mês atuais
    hoje = date.today()
    ano_atual = hoje.year
    mes_atual = hoje.month

    # Determinar o primeiro e o último dia do mês atual
    primeiro_dia_mes = date(ano_atual, mes_atual, 1)
    ultimo_dia_mes = date(ano_atual, mes_atual, calendar.monthrange(ano_atual, mes_atual)[1])

    # Receber dados de Conta, Gasto e Comprovante
    contas = Conta.objects.all()
    gastos = Gasto.objects.filter(data_cadastro__range=(primeiro_dia_mes, ultimo_dia_mes))
    comprovantes = Comprovante.objects.all()

    # Verificar se 'nome_associado' de 'gastos' tem 'nome' de 'contas'
    for conta in contas:
        gasto_associado = gastos.filter(nome_associado=conta.nome)
        if not gasto_associado.exists():
            # Se não houver gastos associados, adicionar informações da conta com alerta 'Boleto'
            dados_relatorio.append({
                'nome': conta.nome,
                'vencimento': conta.vencimento_dia,
                'valor': "",  # Não tem valor associado a uma conta sem gastos
                'id': "",  # Não tem id associado a uma conta sem gastos
                'color': 'Orange',
                'necessario': 'Boleto'
            })

    # Verificar se 'id' de 'gastos' tem em 'id_gasto' de 'comprovantes'
    for gasto in gastos:
        comprovante_associado = comprovantes.filter(id_gasto=gasto.id)
        if not comprovante_associado.exists():
            # Se não houver comprovante associado, adicionar informações do gasto com alerta 'Pagamento'
            dados_relatorio.append({
                'nome': gasto.nome_associado,
                'vencimento': gasto.vencimento_dia,
                'valor': gasto.valor,
                'id': gasto.id,
                'color': 'red',
                'necessario': 'Pagamento'
            })

    return render(request, 'apps/financeiro/table_gastos.html', {'dados_relatorio': dados_relatorio})

def formContas(request):
    conta_form = ContaForm()
    gasto_form = GastoForm()
    contas = Conta.objects.all()

    if request.method == 'POST':
        if 'nome' in request.POST:
            conta_form = ContaForm(request.POST)
            if conta_form.is_valid():
                conta = conta_form.save()
                print("Conta salva com sucesso")
                return redirect('rh:formGastos')
            else:
                print("Erros no formulário de conta:", conta_form.errors)
    context = {
        'conta_form': conta_form,
        'gasto_form': gasto_form,
        'contas': contas,
    }
    return render(request, 'apps/financeiro/form_contas.html', context)