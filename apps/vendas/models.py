from django.db import models

class BaseClientes(models.Model):
    nome = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.nome

class ExtDebitos(models.Model):
    id_cliente = models.ForeignKey(BaseClientes, on_delete=models.CASCADE)
    banco = models.CharField(max_length=255)
    cod_orgao = models.CharField(max_length=255)
    orgao = models.CharField(max_length=255)
    matricula = models.CharField(max_length=255)
    upag = models.CharField(max_length=255)
    valor = models.FloatField()
    margem = models.FloatField()
    margem_cartao = models.FloatField()
    prazo = models.IntegerField()
    situacao = models.CharField(max_length=255)

    class Meta:
        unique_together = ('id_cliente', 'valor', 'margem', 'prazo', 'situacao')

    def __str__(self):
        return f"{self.id_cliente} - {self.valor}"
