from django.db import models
from django.db.models import Sum, F, FloatField
from datetime import date, timedelta
import decimal


class VendasQuerySet(models.QuerySet):
    def visa(self):
        return self.filter(bandeira__nome="Visa")

    def master(self):
        return self.filter(bandeira__nome="Mastercard")

    def amex(self):
        return self.filter(bandeira__nome="American Express")

    def elo(self):
        return self.filter(bandeira__nome="Elo")

    def hiper(self):
        return self.filter(bandeira__nome="Hipercard")

    def debito(self):
        return self.filter(tipo__icontains="Débito")

    def credito(self):
        return self.filter(tipo__icontains="Crédito")

    def credito_vista(self):
        return self.filter(tipo="Crédito à vista")

    def credito_pre(self):
        return self.filter(tipo="Crédito Pré-pago")

    def credito_moeda(self):
        return self.filter(tipo="Crédito conversor moeda")

    def credito_parcelado(self):
        return self.filter(tipo__icontains="Crédito parcelado loja")

    def pendente(self):
        return self.filter(pago=False).filter(contesta=False).filter(arquivado=False)

    def processado(self):
        return self.filter(pago=True).filter(arquivado=False)

    def hoje(self):
        return self.filter(previsao_pgto=date.today())

    def amanha(self):
        return self.filter(previsao_pgto=(date.today()+timedelta(days=1)))

    def total_bruto(self):
        if self.aggregate(tb=Sum(F('valor_bruto')))['tb']:
            return round(decimal.Decimal(self.aggregate(tb=Sum(F('valor_bruto')))['tb']), 2)
        else:
            return "---"

    def total_tarifa(self):
        if self.aggregate(tt=Sum(F('valor_tarifa')))['tt']:
            return round(decimal.Decimal(self.aggregate(tt=Sum(F('valor_tarifa')))['tt']), 2)
        else:
            return "---"

    def total_cobranca(self):
        if self.aggregate(tc=Sum(F('valor_cobranca')))['tc']:
            return round(decimal.Decimal(self.aggregate(tc=Sum(F('valor_cobranca')))['tc']), 2)
        else:
            return "---"

    def total_devido(self):
        if self.aggregate(td=Sum(F('valor_devido')))['td']:
            return round(decimal.Decimal(self.aggregate(td=Sum(F('valor_devido')))['td']), 2)
        else:
            return "---"

    def total_contestado(self):
        if self.aggregate(tc=Sum(F('valor_contestado')))['tc']:
            return round(decimal.Decimal(self.aggregate(tc=Sum(F('valor_contestado')))['tc']), 2)
        else:
            return "---"

    def lucro_total(self):
        if self.aggregate(lt=Sum(F('lucro')))['lt']:
            return round(decimal.Decimal(self.aggregate(lt=Sum(F('lucro')))['lt']), 2)
        else:
            return "---"

    def entrada(self):
        if self.aggregate(en=Sum(F('valor_bruto') - F('valor_tarifa')))['en']:
            return round(decimal.Decimal(self.aggregate(en=Sum(F('valor_bruto') - F('valor_tarifa')))['en']), 2)
        else:
            return "---"


class VendasManager(models.Manager):
    def get_queryset(self):
        return VendasQuerySet(self.model, using=self._db)

    def visa(self):
        return self.get_queryset().visa()

    def master(self):
        return self.get_queryset().master()

    def amex(self):
        return self.get_queryset().amex()

    def elo(self):
        return self.get_queryset().elo()

    def hiper(self):
        return self.get_queryset().hiper()

    def debito(self):
        return self.get_queryset().debito()

    def credito(self):
        return self.get_queryset().credito()

    def credito_vista(self):
        return self.get_queryset().credito_vista()

    def credito_pre(self):
        return self.get_queryset().credito_pre()

    def credito_moeda(self):
        return self.get_queryset().credito_moeda()

    def credito_parcelado(self):
        return self.get_queryset().credito_parcelado()

    def pendente(self):
        return self.get_queryset().pendente()

    def processado(self):
        return self.get_queryset().processado()

    def hoje(self):
        return self.get_queryset().hoje()

    def amanha(self):
        return self.get_queryset().amanha()

    def total_bruto(self):
        return self.get_queryset().total_bruto()

    def total_tarifa(self):
        return self.get_queryset().total_tarifa()

    def total_cobranca(self):
        return self.get_queryset().total_cobranca()

    def total_devido(self):
        return self.get_queryset().total_devido()

    def total_contestado(self):
        return self.get_queryset().total_contestado()

    def lucro_total(self):
        return self.get_queryset().lucro_total()

    def entrada(self):
        return self.get_queryset().entrada()

