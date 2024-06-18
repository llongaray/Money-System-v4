from django.db import models
from datetime import datetime
import os
from apps.recursos_humanos.models import get_setor_choices, get_empresas_choices

# Função para obter os tipos de contas
def get_tipos_choices():
    return [
        ('GERAL', 'Geral'),
        ('SISTEMA', 'Sistema'),
        ('VOIP', 'Voip'),
    ]

# Função para obter os status
def get_status_choices():
    return [
        ('Pago', 'Pago'),
        ('A pagar', 'A pagar'),
    ]

# Função para gerar o nome de arquivo customizado
def custom_filename(instance, filename, folder):
    today = datetime.today()
    timestamp = today.strftime("%d-%H-%M-%S")
    filename = f"{instance.nome_associado}_{timestamp}.pdf"
    return os.path.join(folder, instance.year_month, filename)

class Conta(models.Model):
    nome = models.CharField(max_length=20)
    vencimento_dia = models.IntegerField()

    # Usar a função para obter os tipos de contas
    tipo_conta = models.CharField(max_length=20, choices=get_tipos_choices())

    # Usar SETOR_CHOICES e EMPRESAS_CHOICES importados
    SETOR_CHOICES = get_setor_choices()
    EMPRESAS_CHOICES = get_empresas_choices()

    for choice in SETOR_CHOICES:
        locals()[choice[0].replace(" ", "_")] = models.BooleanField(default=False)
    for choice in EMPRESAS_CHOICES:
        locals()[choice[0].replace(" ", "_")] = models.BooleanField(default=False)

    # Registro automático de DATA:HORA
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Gasto(models.Model):
    def upload_to_custom(instance, filename):
        return custom_filename(instance, filename, 'boletos')
    
    nome_associado = models.CharField(max_length=100)
    valor = models.CharField(max_length=1000000, null=True, blank=True)
    vencimento_dia = models.IntegerField(null=True, blank=True)

    # Usar EMPRESAS_CHOICES importados
    EMPRESAS_CHOICES = get_empresas_choices()
    
    for choice in EMPRESAS_CHOICES:
        locals()[choice[0].replace(" ", "_")] = models.BooleanField(default=False)

    STATUS_CHOICES = get_status_choices()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="A pagar")
    data_cadastro = models.DateTimeField(auto_now_add=True)
    year_month = models.CharField(max_length=7, blank=True, editable=False)

    boleto = models.FileField(upload_to=upload_to_custom)

    def __str__(self):
        return f"Gasto de {self.nome_associado} - R$ {self.valor}"

class Comprovante(models.Model):
    def upload_to_custom(instance, filename):
        return custom_filename(instance, filename, 'comprovantes')
    
    nome_associado = models.CharField(max_length=100)
    valor = models.CharField(max_length=1000000, null=True, blank=True)
    vencimento_dia = models.IntegerField(null=True, blank=True)

    # Usar EMPRESAS_CHOICES importados
    EMPRESAS_CHOICES = get_empresas_choices()
    
    for choice in EMPRESAS_CHOICES:
        locals()[choice[0].replace(" ", "_")] = models.BooleanField(default=False)

    STATUS_CHOICES = get_status_choices()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="A pagar")
    data_cadastro = models.DateTimeField(auto_now_add=True)
    year_month = models.CharField(max_length=7, blank=True, editable=False)

    comprovante = models.FileField(upload_to=upload_to_custom)
    id_gasto = models.CharField(max_length=9999999, blank=True, null=True)

    def __str__(self):
        return f"Comprovante de {self.nome_associado} - R$ {self.valor}"
