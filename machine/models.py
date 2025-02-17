from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from .manager import VendasManager

LISTA_TIPO = (
    ("Débito à vista", "Débito à vista"),
    ("Débito pré-pago", "Débito pré-pago"),
    ("Crédito à vista", "Crédito à vista"),
    ("Crédito pré-pago", "Crédito pré-pago"),
    ("Crédito conversor de moedas", "Crédito conversor de moedas"),
    ("Crédito parcelado loja 2x", "Crédito parcelado loja 2x"),
    ("Crédito parcelado loja 3x", "Crédito parcelado loja 3x"),
    ("Crédito parcelado loja 4x", "Crédito parcelado loja 4x"),
    ("Crédito parcelado loja 5x", "Crédito parcelado loja 5x"),
    ("Crédito parcelado loja 6x", "Crédito parcelado loja 6x"),
    ("Crédito parcelado loja 7x", "Crédito parcelado loja 7x"),
    ("Crédito parcelado loja 8x", "Crédito parcelado loja 8x"),
    ("Crédito parcelado loja 9x", "Crédito parcelado loja 9x"),
    ("Crédito parcelado loja 10x", "Crédito parcelado loja 10x"),
    ("Crédito parcelado loja 11x", "Crédito parcelado loja 11x"),
    ("Crédito parcelado loja 12x", "Crédito parcelado loja 12x"),
)


class Usuario(AbstractUser):
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.username + " - " + self.email


class Estabelecimento(models.Model):
    razao_social = models.CharField(max_length=250, default="Desconhecido")
    codigo = models.CharField(max_length=100, default="0")
    taxa_debito = models.DecimalField(max_digits=5, decimal_places=2, default=3.50)
    taxa_credito = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    usuario = models.ForeignKey(Usuario, related_name="estabelecimento", on_delete=models.PROTECT)

    def __str__(self):
        return self.razao_social


class Operadora(models.Model):
    nome = models.CharField(max_length=250, default="Desconhecido")
    logo = models.ImageField(upload_to='logos', null=True, blank=True)

    def __str__(self):
        return self.nome


class Bandeira(models.Model):
    nome = models.CharField(max_length=250, default="Desconhecido")
    logo = models.ImageField(upload_to='logos', null=True, blank=True)
    debito_vista = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    debito_pre = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_vista = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_pre = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_2x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_3x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_4x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_5x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_6x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_7x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_8x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_9x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_10x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_11x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_12x = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    credito_moeda = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    operadora = models.ForeignKey(Operadora, related_name="bandeira", on_delete=models.PROTECT)

    def __str__(self):
        return self.nome + " - " + self.operadora.nome


class Venda(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, related_name="venda", on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=50,
        choices=LISTA_TIPO,
        default="Crédito à vista",
    )
    bandeira = models.ForeignKey(Bandeira, related_name="venda", on_delete=models.PROTECT)
    data_venda = models.DateTimeField(default=timezone.now)
    previsao_pgto = models.DateField("Previsão de pagamento", default=timezone.now)
    valor_bruto = models.DecimalField("Valor da venda", max_digits=8, decimal_places=2, default=0.00)
    taxa = models.DecimalField("Sua taxa", max_digits=8, decimal_places=2, default=0.00)
    valor_tarifa = models.DecimalField("Valor da tarifa da operadora", max_digits=8, decimal_places=2, default=0.00)
    valor_cobranca = models.DecimalField("Valor a ser cobrado", max_digits=8, decimal_places=2, default=0.00)
    valor_devido = models.DecimalField("Valor devido ao cliente", max_digits=8, decimal_places=2, default=0.00)
    lucro = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    nr_maquina = models.CharField(max_length=40, null=True, blank=True)
    cod_venda = models.CharField(max_length=70, null=True, blank=True)
    em_conta = models.BooleanField(default=False)
    pago = models.BooleanField(default=False)
    arquivado = models.BooleanField(default=False)
    contesta = models.BooleanField(default=False)
    valor_contestado = models.DecimalField("Valor cobrado pela operadora", max_digits=8, decimal_places=2, default=0.00)
    objects = VendasManager()

    def __str__(self):
        return str(self.data_venda) + " - " + str(self.tipo) + " - " + str(self.valor_bruto)


class Atualizacao(models.Model):
    nome = models.CharField(max_length=50)
    vigente = models.BooleanField(default=True)
    arquivo = models.FileField(upload_to='arquivos')
    estabelecimento = models.ForeignKey(Estabelecimento, related_name="atualizacao", on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

