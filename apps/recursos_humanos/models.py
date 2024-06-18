from django.db import models

# Funções para retornar os choices
def get_tipo_contrato_choices():
    return [
        ('Estágio', 'Estágio'),
        ('CLT', 'CLT'),
        ('PJ', 'PJ'),
    ]

def get_turno_choices():
    return [
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
        ('Integral', 'Integral'),
    ]

def get_tempo_contrato_choices():
    return [
        ('6 Meses', '6 Meses'),
        ('1 Ano', '1 Ano'),
        ('2 Anos', '2 Anos'),
        ('Indeterminado', 'Indeterminado'),
    ]

def get_horario_diario_choices():
    return [
        ('6 Horas', '6 Horas'),
        ('9 Horas', '9 Horas'),
    ]

def get_setor_choices():
    return [
        ('Loja', 'Loja'),
        ('SIAPE', 'SIAPE'),
        ('INSS', 'INSS'),
        ('TI', 'TI'),
        ('Marketing', 'Marketing'),
        ('Operacional', 'Operacional'),
        ('Outros', 'Outros'),
    ]

def get_empresas_choices():
    return [
        ('Money POA', 'Money POA'),
        ('Money SLE', 'Money SLE'),
        ('Money SM', 'Money SM'),
        ('Park Guaiba', 'Park Guaiba'),
    ]

def get_status_atividade_choices():
    return [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]

class Funcionario(models.Model):
    # Informações pessoais
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14) 
    cnpj = models.CharField(max_length=18, blank=True, default='--/--')  # CNPJ é opcional e tem um valor padrão
    
    # Tipo de contrato
    tipo_contrato = models.CharField(max_length=10, choices=get_tipo_contrato_choices())
    
    # Duração do contrato
    tempo_contrato = models.CharField(max_length=15, choices=get_tempo_contrato_choices())

    # Detalhes do horário de trabalho
    turno = models.CharField(max_length=10, choices=get_turno_choices(), null=True)  # Pode ser nulo se não aplicável
    horario_diario = models.CharField(max_length=8, choices=get_horario_diario_choices(), null=True)  # Pode ser nulo se não aplicável

    # Remuneração e benefícios
    salario = models.DecimalField(max_digits=10, decimal_places=2)  
    vr_ativo = models.BooleanField(default=False)
    vr_valor_diario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Valor diário do VR, pode ser nulo
    vt_ativo = models.BooleanField(default=False)
    vt_valor_diario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Valor diário do VT, pode ser nulo

    # Departamento e empresa
    setor = models.CharField(max_length=20, choices=get_setor_choices())
    empresa = models.CharField(max_length=20, choices=get_empresas_choices(), null=True)

    # Status do funcionário
    status_atividade = models.CharField(max_length=7, choices=get_status_atividade_choices())
    
    # Data de cadastro automaticamente adicionada
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.pk} - Nome: {self.nome_completo} - Status: {self.status_atividade}"
