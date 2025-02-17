
import decimal
from .models import (Bandeira,
                     Estabelecimento,
                     Venda,
                     Operadora)
from datetime import timedelta
import pandas as pd


def calculo_valor_bruto(numero):
    x = round(numero, 2)
    return x


def calculo_valor_cobranca(numero, taxa):
    x = round(numero * taxa / 100, 2)
    return x


def calculo_valor_devido(numero, taxa):
    x = round(numero - (numero * taxa) / 100, 2)
    return x


def calculo_valor_tarifa(numero, taxa):
    x = round(numero * taxa / 100, 2)
    return x


def calculo_lucro(numero, taxa1, taxa2):
    x = round(numero * taxa1 / 100 - numero * taxa2 / 100, 2)
    return x


def calculo_valor_descontado(numero1):
    x = round(decimal.Decimal(numero1), 2)
    return x


def inserir_dados_cielo(request, d_records, pk, operadora):
    op = Operadora.objects.get(nome=operadora)
    estabelecimento = Estabelecimento.objects.get(id=pk)
    h = timedelta(seconds=10800)
    list_vendas = []
    for dado in d_records:
        bandeira = Bandeira.objects.get(nome=str(dado['Bandeira']), operadora=op)
        usuario_logado = request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado)
        numero = decimal.Decimal(dado['Valor bruto'])
        numero1 = decimal.Decimal(str(dado['Taxa/tarifa']).replace('-', ''))
        data_v = str(dado['Data da venda'] + ' ' + dado['Hora da venda'])
        if not vendas.filter(cod_venda=dado['Código da venda']):
            if 'édito' in dado['Forma de pagamento']:
                if dado['Forma de pagamento'] == "Crédito à vista":
                    v = Venda(estabelecimento=estabelecimento,
                              tipo=dado['Forma de pagamento'],
                              bandeira=bandeira,
                              data_venda=pd.to_datetime(data_v, format='%d/%m/%Y %H:%M') - h,
                              previsao_pgto=pd.to_datetime(dado['Data prevista do pagamento'], format='%d/%m/%Y'),
                              valor_bruto=calculo_valor_bruto(numero),
                              taxa=estabelecimento.taxa_credito,
                              valor_tarifa=calculo_valor_descontado(numero1),
                              valor_cobranca=calculo_valor_cobranca(numero, estabelecimento.taxa_credito),
                              valor_devido=calculo_valor_devido(numero, estabelecimento.taxa_credito),
                              lucro=calculo_lucro(numero, estabelecimento.taxa_credito, bandeira.credito_vista),
                              nr_maquina=dado['Número da máquina'],
                              cod_venda=dado['Código da venda'])
                    list_vendas.append(v)
                elif dado['Forma de pagamento'] == "Crédito parcelado loja":
                    num = int(dado['Quantidade total de parcelas'])
                    if num == 2:
                        taxa = bandeira.credito_2x
                    elif num == 3:
                        taxa = bandeira.credito_3x
                    elif num == 4:
                        taxa = bandeira.credito_4x
                    elif num == 5:
                        taxa = bandeira.credito_5x
                    elif num == 6:
                        taxa = bandeira.credito_6x
                    elif num == 7:
                        taxa = bandeira.credito_7x
                    elif num == 8:
                        taxa = bandeira.credito_8x
                    elif num == 9:
                        taxa = bandeira.credito_9x
                    elif num == 10:
                        taxa = bandeira.credito_10x
                    elif num == 11:
                        taxa = bandeira.credito_11x
                    elif num == 12:
                        taxa = bandeira.credito_12x
                    v = Venda(estabelecimento=estabelecimento,
                              tipo=dado['Forma de pagamento'],
                              bandeira=bandeira,
                              data_venda=pd.to_datetime(data_v, format='%d/%m/%Y %H:%M') - h,
                              previsao_pgto=pd.to_datetime(dado['Data prevista do pagamento'], format='%d/%m/%Y'),
                              valor_bruto=calculo_valor_bruto(numero),
                              taxa=estabelecimento.taxa_credito,
                              valor_tarifa=calculo_valor_descontado(numero1),
                              valor_cobranca=calculo_valor_cobranca(numero, estabelecimento.taxa_credito),
                              valor_devido=calculo_valor_devido(numero, estabelecimento.taxa_credito),
                              lucro=calculo_lucro(numero, estabelecimento.taxa_credito, taxa),
                              nr_maquina=dado['Número da máquina'],
                              cod_venda=dado['Código da venda'])
                    list_vendas.append(v)
                elif dado['Forma de pagamento'] == "Crédito pré-pago":
                    v = Venda(estabelecimento=estabelecimento,
                              tipo=dado['Forma de pagamento'],
                              bandeira=bandeira,
                              data_venda=pd.to_datetime(data_v, format='%d/%m/%Y %H:%M') - h,
                              previsao_pgto=pd.to_datetime(dado['Data prevista do pagamento'], format='%d/%m/%Y'),
                              valor_bruto=calculo_valor_bruto(numero),
                              taxa=estabelecimento.taxa_credito,
                              valor_tarifa=calculo_valor_descontado(numero1),
                              valor_cobranca=calculo_valor_cobranca(numero, estabelecimento.taxa_credito),
                              valor_devido=calculo_valor_devido(numero, estabelecimento.taxa_credito),
                              lucro=calculo_lucro(numero, estabelecimento.taxa_credito, bandeira.credito_pre),
                              nr_maquina=dado['Número da máquina'],
                              cod_venda=dado['Código da venda'])
                    list_vendas.append(v)
                else:
                    v = Venda(estabelecimento=estabelecimento,
                              tipo=dado['Forma de pagamento'],
                              bandeira=bandeira,
                              data_venda=pd.to_datetime(data_v, format='%d/%m/%Y %H:%M') - h,
                              previsao_pgto=pd.to_datetime(dado['Data prevista do pagamento'], format='%d/%m/%Y'),
                              valor_bruto=calculo_valor_bruto(numero),
                              taxa=estabelecimento.taxa_credito,
                              valor_tarifa=calculo_valor_descontado(numero1),
                              valor_cobranca=calculo_valor_cobranca(numero, estabelecimento.taxa_credito),
                              valor_devido=calculo_valor_devido(numero, estabelecimento.taxa_credito),
                              lucro=calculo_lucro(numero, estabelecimento.taxa_credito, bandeira.credito_moeda),
                              nr_maquina=dado['Número da máquina'],
                              cod_venda=dado['Código da venda'])
                    list_vendas.append(v)
            else:
                if dado['Forma de pagamento'] == "Débito à vista":
                    v = Venda(estabelecimento=estabelecimento,
                              tipo=dado['Forma de pagamento'],
                              bandeira=bandeira,
                              data_venda=pd.to_datetime(data_v, format='%d/%m/%Y %H:%M') - h,
                              previsao_pgto=pd.to_datetime(dado['Data prevista do pagamento'], format='%d/%m/%Y'),
                              valor_bruto=calculo_valor_bruto(numero),
                              taxa=estabelecimento.taxa_debito,
                              valor_tarifa=calculo_valor_descontado(numero1),
                              valor_cobranca=calculo_valor_cobranca(numero, estabelecimento.taxa_debito),
                              valor_devido=calculo_valor_devido(numero, estabelecimento.taxa_debito),
                              lucro=calculo_lucro(numero, estabelecimento.taxa_debito, bandeira.debito_vista),
                              nr_maquina=dado['Número da máquina'],
                              cod_venda=dado['Código da venda'])
                    list_vendas.append(v)
                else:
                    v = Venda(estabelecimento=estabelecimento,
                              tipo=dado['Forma de pagamento'],
                              bandeira=bandeira,
                              data_venda=pd.to_datetime(data_v, format='%d/%m/%Y %H:%M') - h,
                              previsao_pgto=pd.to_datetime(dado['Data prevista do pagamento'], format='%d/%m/%Y'),
                              valor_bruto=calculo_valor_bruto(numero),
                              taxa=estabelecimento.taxa_debito,
                              valor_tarifa=calculo_valor_descontado(numero1),
                              valor_cobranca=calculo_valor_cobranca(numero, estabelecimento.taxa_debito),
                              valor_devido=calculo_valor_devido(numero, estabelecimento.taxa_debito),
                              lucro=calculo_lucro(numero, estabelecimento.taxa_debito, bandeira.debito_pre),
                              nr_maquina=dado['Número da máquina'],
                              cod_venda=dado['Código da venda'])
                    list_vendas.append(v)
    Venda.objects.bulk_create(list_vendas)
    for dado in d_records:
        numero = decimal.Decimal(dado['Valor da venda'])
        venda = Venda.objects.filter(cod_venda=dado['Código da venda'],
                                     valor_bruto=calculo_valor_bruto(numero))
        if venda:
            venda = Venda.objects.get(cod_venda=dado['Código da venda'],
                                      valor_bruto=calculo_valor_bruto(numero))
            if venda.lucro / venda.valor_bruto <= 0.01:
                venda.lucro = decimal.Decimal(
                    (float(venda.valor_tarifa / venda.valor_bruto) + 0.03) * float(venda.valor_bruto))
                venda.save()


def inserir_dados_cpay(request, d_records, pk, operadora):
    op = Operadora.objects.get(nome=operadora)
    estabelecimento = Estabelecimento.objects.get(id=pk)
    h = timedelta(seconds=10800)
    list_vendas = []
    for dado in d_records:
        bandeira = Bandeira.objects.get(nome=str(dado['Bandeira do cartão']), operadora=op)
        usuario_logado = request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado)
        numero = decimal.Decimal(dado['Valor da venda'])
        data_v = str(dado['Data da venda'])
        if not vendas.filter(cod_venda=dado['Código da venda']):
            if 'édito' in dado['Tipo de operação']:
                if str(dado['Parcelas']) == "1.0":
                    taxa = bandeira.credito_vista
                    v = Venda(estabelecimento=estabelecimento,
                              tipo="Crédito à vista",
                              bandeira=bandeira,
                              data_venda=pd.to_datetime(data_v, format='%Y/%m/%d %H:%M') - h,
                              previsao_pgto=pd.to_datetime(data_v, format='%Y/%m/%d %H:%M') - h,
                              valor_bruto=calculo_valor_bruto(numero),
                              taxa=estabelecimento.taxa_credito,
                              valor_tarifa=calculo_valor_tarifa(numero, taxa),
                              valor_cobranca=calculo_valor_cobranca(numero, estabelecimento.taxa_credito),
                              valor_devido=calculo_valor_devido(numero, estabelecimento.taxa_credito),
                              lucro=calculo_lucro(numero, estabelecimento.taxa_credito, taxa),
                              nr_maquina=dado['Terminal ID'],
                              cod_venda=dado['Código da venda'])
                    list_vendas.append(v)
                elif str(dado['Parcelas']) == "2.0":
                    taxa = bandeira.credito_2x
                    v = Venda(estabelecimento=estabelecimento,
                              tipo="Crédito parcelado loja 2x",
                              bandeira=bandeira,
                              data_venda=pd.to_datetime(data_v, format='%Y/%m/%d %H:%M') - h,
                              previsao_pgto=pd.to_datetime(data_v, format='%Y/%m/%d %H:%M') - h,
                              valor_bruto=calculo_valor_bruto(numero),
                              taxa=estabelecimento.taxa_credito,
                              valor_tarifa=calculo_valor_tarifa(numero, taxa),
                              valor_cobranca=calculo_valor_cobranca(numero, estabelecimento.taxa_credito),
                              valor_devido=calculo_valor_devido(numero, estabelecimento.taxa_credito),
                              lucro=calculo_lucro(numero, estabelecimento.taxa_credito, taxa),
                              nr_maquina=dado['Terminal ID'],
                              cod_venda=dado['Código da venda'])
                    list_vendas.append(v)
            else:
                if dado['Tipo de operação'] == "Débito":
                    taxa = bandeira.debito_vista
                    v = Venda(estabelecimento=estabelecimento,
                              tipo="Débito à vista",
                              bandeira=bandeira,
                              data_venda=pd.to_datetime(data_v, format='%Y/%m/%d %H:%M') - h,
                              previsao_pgto=pd.to_datetime(data_v, format='%Y/%m/%d %H:%M') - h,
                              valor_bruto=calculo_valor_bruto(numero),
                              taxa=estabelecimento.taxa_debito,
                              valor_tarifa=calculo_valor_tarifa(numero, taxa),
                              valor_cobranca=calculo_valor_cobranca(numero, estabelecimento.taxa_debito),
                              valor_devido=calculo_valor_devido(numero, estabelecimento.taxa_debito),
                              lucro=calculo_lucro(numero, estabelecimento.taxa_debito, taxa),
                              nr_maquina=dado['Terminal ID'],
                              cod_venda=dado['Código da venda'])
                    list_vendas.append(v)
    Venda.objects.bulk_create(list_vendas)
    for dado in d_records:
        numero = decimal.Decimal(dado['Valor da venda'])
        venda = Venda.objects.filter(cod_venda=dado['Código da venda'],
                                     valor_bruto=calculo_valor_bruto(numero))
        if venda:
            venda = Venda.objects.get(cod_venda=dado['Código da venda'],
                                      valor_bruto=calculo_valor_bruto(numero))
            if venda.lucro / venda.valor_bruto <= 0.01:
                venda.lucro = decimal.Decimal(
                    (float(venda.lucro / venda.valor_bruto) + 0.03) * float(venda.valor_bruto))
                venda.valor_cobranca = venda.lucro + venda.valor_tarifa
                venda.valor_devido = venda.valor_bruto - venda.valor_cobranca
                venda.taxa = 0
                venda.save()



