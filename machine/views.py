import decimal
from django.shortcuts import render, reverse, redirect
from django.shortcuts import reverse
from django.db.models import Sum, F
from django.views.generic import (ListView, \
    CreateView, \
    DetailView, \
    UpdateView, \
    TemplateView,
    FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (Venda,
                     Estabelecimento,
                     Usuario,
                     Bandeira,
                     Operadora)
from .forms import FormHomepage
import pandas as pd


class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('machine:dashboardpendentes')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get("email")
        us = Usuario.objects.filter(email=email)
        if us:
            return reverse('machine:login')
        else:
            return reverse('machine:acessonegado')


class AcessoNegado(TemplateView):
    template_name = "acessonegado.html"


class Dashboardpendentes(TemplateView):
    template_name = "dashboardpendentes.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboardpendentes, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(pago=False)
        total_bruto = vendas.aggregate(tb=Sum(F('valor_bruto')))['tb']
        total_tarifa = vendas.aggregate(tt=Sum(F('valor_tarifa')))['tt']
        total_cobranca = vendas.aggregate(tc=Sum(F('valor_cobranca')))['tc']
        total_devido = vendas.aggregate(td=Sum(F('valor_devido')))['td']
        lucro_total = vendas.aggregate(lt=Sum(F('lucro')))['lt']
        if total_bruto:
            texto_bruto = f'R$ {total_bruto:.2f}'
        else:
            texto_bruto = "-"
        if total_tarifa:
            texto_tarifa = f'R$ {total_tarifa:.2f}'
        else:
            texto_tarifa = "-"
        if total_cobranca:
            texto_cobranca = f'R$ {total_cobranca:.2f}'
        else:
            texto_cobranca = "-"
        if total_devido:
            texto_devido = f'R$ {total_devido:.2f}'
        else:
            texto_devido = "-"
        if lucro_total:
            texto_lucro = f'R$ {lucro_total:.2f}'
        else:
            texto_lucro = "-"
        if total_bruto and total_tarifa:
            entrada = total_bruto - total_tarifa
            texto_entrada = f'R$ {entrada:.2f}'
        else:
            texto_entrada = "-"
        context["vendas"] = vendas
        context["texto_bruto"] = texto_bruto
        context["texto_tarifa"] = texto_tarifa
        context["texto_cobranca"] = texto_cobranca
        context["texto_devido"] = texto_devido
        context["lucro_total"] = texto_lucro
        context["texto_entrada"] = texto_entrada
        return context


class Dashboardcontestados(LoginRequiredMixin, TemplateView):
    template_name = "dashboardcontestados.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboardcontestados, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(contesta=True)
        total_bruto = vendas.aggregate(tb=Sum(F('valor_bruto')))['tb']
        total_tarifa = vendas.aggregate(tt=Sum(F('valor_tarifa')))['tt']
        total_cobranca = vendas.aggregate(tc=Sum(F('valor_cobranca')))['tc']
        total_devido = vendas.aggregate(td=Sum(F('valor_devido')))['td']
        lucro_total = vendas.aggregate(lt=Sum(F('lucro')))['lt']
        if total_bruto:
            texto_bruto = f'R$ {total_bruto:.2f}'
        else:
            texto_bruto = "-"
        if total_tarifa:
            texto_tarifa = f'R$ {total_tarifa:.2f}'
        else:
            texto_tarifa = "-"
        if total_cobranca:
            texto_cobranca = f'R$ {total_cobranca:.2f}'
        else:
            texto_cobranca = "-"
        if total_devido:
            texto_devido = f'R$ {total_devido:.2f}'
        else:
            texto_devido = "-"
        if lucro_total:
            texto_lucro = f'R$ {lucro_total:.2f}'
        else:
            texto_lucro = "-"
        context["vendas"] = vendas
        context["texto_bruto"] = texto_bruto
        context["texto_tarifa"] = texto_tarifa
        context["texto_cobranca"] = texto_cobranca
        context["texto_devido"] = texto_devido
        context["lucro_total"] = texto_lucro
        return context


class Dashboardprocessados(LoginRequiredMixin, TemplateView):
    template_name = "dashboardprocessados.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboardprocessados, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(pago=True).filter(arquivado=False)
        total_bruto = vendas.aggregate(tb=Sum(F('valor_bruto')))['tb']
        total_tarifa = vendas.aggregate(tt=Sum(F('valor_tarifa')))['tt']
        total_cobranca = vendas.aggregate(tc=Sum(F('valor_cobranca')))['tc']
        total_devido = vendas.aggregate(td=Sum(F('valor_devido')))['td']
        lucro_total = vendas.aggregate(lt=Sum(F('lucro')))['lt']
        if total_bruto:
            texto_bruto = f'R$ {total_bruto:.2f}'
        else:
            texto_bruto = "-"
        if total_tarifa:
            texto_tarifa = f'R$ {total_tarifa:.2f}'
        else:
            texto_tarifa = "-"
        if total_cobranca:
            texto_cobranca = f'R$ {total_cobranca:.2f}'
        else:
            texto_cobranca = "-"
        if total_devido:
            texto_devido = f'R$ {total_devido:.2f}'
        else:
            texto_devido = "-"
        if lucro_total:
            texto_lucro = f'R$ {lucro_total:.2f}'
        else:
            texto_lucro = "-"
        if total_bruto and total_tarifa:
            entrada = total_bruto - total_tarifa
            texto_entrada = f'R$ {entrada:.2f}'
        else:
            texto_entrada = "-"
        context["vendas"] = vendas
        context["texto_bruto"] = texto_bruto
        context["texto_tarifa"] = texto_tarifa
        context["texto_cobranca"] = texto_cobranca
        context["texto_devido"] = texto_devido
        context["lucro_total"] = texto_lucro
        context["texto_entrada"] = texto_entrada
        return context


def ajusta_contestados(request, id):
    venda = Venda.objects.get(id=id)
    venda.valor_tarifa = venda.valor_contestado
    venda.contesta = False
    venda.save()
    return redirect('machine:dashboardcontestados')


def confirma_pgto(request, id):
    venda = Venda.objects.get(id=id)
    venda.pago = True
    venda.save()
    return redirect('machine:dashboardpendentes')


def cancela_pgto(request, id):
    venda = Venda.objects.get(id=id)
    venda.pago = False
    venda.save()
    return redirect('machine:dashboardprocessados')


class Readestabelecimento(LoginRequiredMixin, TemplateView):
    template_name = "readestabelecimento.html"

    def get_context_data(self, **kwargs):
        context = super(Readestabelecimento, self).get_context_data(**kwargs)
        clientes = self.request.user.estabelecimento.all()
        context['clientes'] = clientes
        return context


class Readvendas(LoginRequiredMixin, TemplateView):
    template_name = "readvendas.html"

    def get_context_data(self, **kwargs):
        context = super(Readvendas, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado)
        context['vendas'] = vendas
        return context


class Createestabelecimento(LoginRequiredMixin, CreateView):
    template_name = "createestabelecimento.html"
    model = Estabelecimento
    fields = ['razao_social', 'codigo', 'taxa_debito', 'taxa_credito']

    def get_context_data(self, **kwargs):
        context = super(Createestabelecimento, self).get_context_data(**kwargs)
        clientes = self.request.user.estabelecimento.all()
        context['clientes'] = clientes
        return context

    def form_valid(self, form):
        usu = self.request.user
        form.instance.usuario = usu
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('machine:readestabelecimentos')


class Createvenda(LoginRequiredMixin, CreateView):
    template_name = "createvenda.html"
    model = Venda
    fields = ['estabelecimento', 'tipo',
              'bandeira', 'data_venda',
              'previsao_pgto', 'valor_bruto',
              'nr_maquina', 'cod_venda']

    def form_valid(self, form):
        if form.instance.tipo == "Débito à vista":
            form.instance.taxa = form.instance.bandeira.debito_vista
        elif form.instance.tipo == "Débito Pré-pago":
            form.instance.taxa = form.instance.bandeira.debito_pre
        elif form.instance.tipo == "Crédito à vista":
            form.instance.taxa = form.instance.bandeira.credito_vista
        elif form.instance.tipo == "Crédito Pré-pago":
            form.instance.taxa = form.instance.bandeira.credito_pre
        elif form.instance.tipo == "Crédito parcelado loja 2x":
            form.instance.taxa = form.instance.bandeira.credito_2x
        elif form.instance.tipo == "Crédito parcelado loja 3x":
            form.instance.taxa = form.instance.bandeira.credito_3x
        elif form.instance.tipo == "Crédito parcelado loja 4x":
            form.instance.taxa = form.instance.bandeira.credito_4x
        elif form.instance.tipo == "Crédito parcelado loja 5x":
            form.instance.taxa = form.instance.bandeira.credito_5x
        elif form.instance.tipo == "Crédito parcelado loja 6x":
            form.instance.taxa = form.instance.bandeira.credito_6x
        elif form.instance.tipo == "Crédito parcelado loja 7x":
            form.instance.taxa = form.instance.bandeira.credito_7x
        elif form.instance.tipo == "Crédito parcelado loja 8x":
            form.instance.taxa = form.instance.bandeira.credito_8x
        elif form.instance.tipo == "Crédito parcelado loja 9x":
            form.instance.taxa = form.instance.bandeira.credito_9x
        elif form.instance.tipo == "Crédito parcelado loja 10x":
            form.instance.taxa = form.instance.bandeira.credito_10x
        elif form.instance.tipo == "Crédito parcelado loja 11x":
            form.instance.taxa = form.instance.bandeira.credito_11x
        elif form.instance.tipo == "Crédito parcelado loja 12x":
            form.instance.taxa = form.instance.bandeira.credito_12x

        valor_tarifa = round(form.instance.valor_bruto * form.instance.taxa / 100, 2)
        form.instance.valor_tarifa = decimal.Decimal(valor_tarifa)

        if "Débito" in form.instance.tipo:
            valor_cobranca = round(form.instance.valor_bruto * form.instance.estabelecimento.taxa_debito / 100, 2)
            form.instance.valor_cobranca = decimal.Decimal(valor_cobranca)
        else:
            valor_cobranca = round(form.instance.valor_bruto * form.instance.estabelecimento.taxa_credito / 100, 2)
            form.instance.valor_cobranca = decimal.Decimal(valor_cobranca)

        valor_devido = round(form.instance.valor_bruto - form.instance.valor_cobranca, 2)
        form.instance.valor_devido = decimal.Decimal(valor_devido)

        lucro = round(form.instance.valor_cobranca - form.instance.valor_tarifa, 2)
        form.instance.lucro = decimal.Decimal(lucro)

        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Createvenda, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado)
        context['vendas'] = vendas
        return context

    def get_success_url(self):
        return reverse('machine:readvendas')


class Updatevenda(LoginRequiredMixin, UpdateView):
    template_name = "updatevenda.html"
    model = Venda
    fields = ['estabelecimento', 'tipo',
              'bandeira', 'data_venda',
              'previsao_pgto', 'valor_bruto',
              'nr_maquina', 'cod_venda']

    def form_valid(self, form):
        if form.instance.tipo == "Débito à vista":
            form.instance.taxa = form.instance.bandeira.debito_vista
        elif form.instance.tipo == "Débito Pré-pago":
            form.instance.taxa = form.instance.bandeira.debito_pre
        elif form.instance.tipo == "Crédito à vista":
            form.instance.taxa = form.instance.bandeira.credito_vista
        elif form.instance.tipo == "Crédito Pré-pago":
            form.instance.taxa = form.instance.bandeira.credito_pre
        elif form.instance.tipo == "Crédito parcelado loja 2x":
            form.instance.taxa = form.instance.bandeira.credito_2x
        elif form.instance.tipo == "Crédito parcelado loja 3x":
            form.instance.taxa = form.instance.bandeira.credito_3x
        elif form.instance.tipo == "Crédito parcelado loja 4x":
            form.instance.taxa = form.instance.bandeira.credito_4x
        elif form.instance.tipo == "Crédito parcelado loja 5x":
            form.instance.taxa = form.instance.bandeira.credito_5x
        elif form.instance.tipo == "Crédito parcelado loja 6x":
            form.instance.taxa = form.instance.bandeira.credito_6x
        elif form.instance.tipo == "Crédito parcelado loja 7x":
            form.instance.taxa = form.instance.bandeira.credito_7x
        elif form.instance.tipo == "Crédito parcelado loja 8x":
            form.instance.taxa = form.instance.bandeira.credito_8x
        elif form.instance.tipo == "Crédito parcelado loja 9x":
            form.instance.taxa = form.instance.bandeira.credito_9x
        elif form.instance.tipo == "Crédito parcelado loja 10x":
            form.instance.taxa = form.instance.bandeira.credito_10x
        elif form.instance.tipo == "Crédito parcelado loja 11x":
            form.instance.taxa = form.instance.bandeira.credito_11x
        elif form.instance.tipo == "Crédito parcelado loja 12x":
            form.instance.taxa = form.instance.bandeira.credito_12x

        valor_tarifa = round(form.instance.valor_bruto * form.instance.taxa / 100, 2)
        form.instance.valor_tarifa = decimal.Decimal(valor_tarifa)

        if "Débito" in form.instance.tipo:
            valor_cobranca = round(form.instance.valor_bruto * form.instance.estabelecimento.taxa_debito / 100, 2)
            form.instance.valor_cobranca = decimal.Decimal(valor_cobranca)
        else:
            valor_cobranca = round(form.instance.valor_bruto * form.instance.estabelecimento.taxa_credito / 100, 2)
            form.instance.valor_cobranca = decimal.Decimal(valor_cobranca)

        valor_devido = round(form.instance.valor_bruto - form.instance.valor_cobranca, 2)
        form.instance.valor_devido = decimal.Decimal(valor_devido)

        lucro = round(form.instance.valor_cobranca - form.instance.valor_tarifa, 2)
        form.instance.lucro = decimal.Decimal(lucro)

        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Updatevenda, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado)
        context['vendas'] = vendas
        return context

    def get_success_url(self):
        return reverse('machine:readvendas')


class Updateestabelecimento(LoginRequiredMixin, UpdateView):
    template_name = "updateestabelecimento.html"
    model = Estabelecimento
    fields = ['razao_social', 'codigo', 'taxa_debito', 'taxa_credito']

    def get_context_data(self, **kwargs):
        context = super(Updateestabelecimento, self).get_context_data(**kwargs)
        clientes = self.request.user.estabelecimento.all()
        context['clientes'] = clientes
        return context

    def get_success_url(self):
        return reverse('machine:readestabelecimentos')


"""def verifica_dados(request):
    dataframe = pd.read_csv('media/vendas1.csv', sep=';', encoding='latin1', engine='python')
    d_records = dataframe.to_dict("records")
    estabelecimento = Estabelecimento.objects.last()
    for dado in d_records:
        if """


def create_dados(request):
    dataframe = pd.read_excel('media/vendas1.xlsx')
    d_records = dataframe.to_dict("records")
    estabelecimento = Estabelecimento.objects.last()
    list_vendas = []
    for dado in d_records:
        bandeira = Bandeira.objects.get(nome=str(dado['Bandeira']))
        if 'édito' in dado['Forma de pagamento']:
            if dado['Forma de pagamento'] == "Crédito à vista":
                v = Venda(estabelecimento=estabelecimento,
                          tipo=dado['Forma de pagamento'],
                          bandeira=bandeira,
                          data_venda=pd.to_datetime(dado['Data da venda'], format='%d/%m/%Y %H:%M'),
                          previsao_pgto=pd.to_datetime(dado['Previsão de pagamento'], format='%d/%m/%Y'),
                          valor_bruto=round(round(decimal.Decimal(dado['Valor da venda']), 2), 2),
                          taxa=estabelecimento.taxa_credito,
                          valor_tarifa=round(
                              round(decimal.Decimal(dado['Valor da venda']) * bandeira.credito_vista) / 100, 2),
                          valor_cobranca=round(round(decimal.Decimal(
                              dado['Valor da venda']) * estabelecimento.taxa_credito) / 100, 2),
                          valor_devido=round(round(decimal.Decimal(dado['Valor da venda'])) - round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_credito) / 100, 2),
                          lucro=round(round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_credito) / 100 - round(
                              decimal.Decimal(dado['Valor da venda']) * bandeira.credito_vista) / 100, 2),
                          nr_maquina=dado['Número da máquina'],
                          cod_venda=dado['Código da venda'])
                list_vendas.append(v)
            elif dado['Forma de pagamento'] == "Crédito parcelado loja":
                v = Venda(estabelecimento=estabelecimento,
                          tipo=dado['Forma de pagamento'],
                          bandeira=bandeira,
                          data_venda=pd.to_datetime(dado['Data da venda'], format='%d/%m/%Y %H:%M'),
                          previsao_pgto=pd.to_datetime(dado['Previsão de pagamento'], format='%d/%m/%Y'),
                          valor_bruto=round(round(decimal.Decimal(dado['Valor da venda']), 2), 2),
                          taxa=estabelecimento.taxa_credito,
                          valor_tarifa=round(
                              round(decimal.Decimal(dado['Valor da venda']) * bandeira.credito_2x) / 100, 2),
                          valor_cobranca=round(round(decimal.Decimal(
                              dado['Valor da venda']) * estabelecimento.taxa_credito) / 100, 2),
                          valor_devido=round(round(decimal.Decimal(dado['Valor da venda'])) - round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_credito) / 100, 2),
                          lucro=round(round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_credito) / 100 - round(
                              decimal.Decimal(dado['Valor da venda']) * bandeira.credito_2x) / 100, 2),
                          nr_maquina=dado['Número da máquina'],
                          cod_venda=dado['Código da venda'])
                list_vendas.append(v)
            elif dado['Forma de pagamento'] == "Pré-pago crédito":
                v = Venda(estabelecimento=estabelecimento,
                          tipo=dado['Forma de pagamento'],
                          bandeira=bandeira,
                          data_venda=pd.to_datetime(dado['Data da venda'], format='%d/%m/%Y %H:%M'),
                          previsao_pgto=pd.to_datetime(dado['Previsão de pagamento'], format='%d/%m/%Y'),
                          valor_bruto=round(round(decimal.Decimal(dado['Valor da venda']), 2), 2),
                          taxa=estabelecimento.taxa_credito,
                          valor_tarifa=round(
                              round(decimal.Decimal(dado['Valor da venda']) * bandeira.credito_pre) / 100, 2),
                          valor_cobranca=round(round(decimal.Decimal(
                              dado['Valor da venda']) * estabelecimento.taxa_credito) / 100, 2),
                          valor_devido=round(round(decimal.Decimal(dado['Valor da venda'])) - round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_credito) / 100, 2),
                          lucro=round(round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_credito) / 100 - round(
                              decimal.Decimal(dado['Valor da venda']) * bandeira.credito_pre) / 100, 2),
                          nr_maquina=dado['Número da máquina'],
                          cod_venda=dado['Código da venda'])
                list_vendas.append(v)
            else:
                v = Venda(estabelecimento=estabelecimento,
                          tipo=dado['Forma de pagamento'],
                          bandeira=bandeira,
                          data_venda=pd.to_datetime(dado['Data da venda'], format='%d/%m/%Y %H:%M'),
                          previsao_pgto=pd.to_datetime(dado['Previsão de pagamento'], format='%d/%m/%Y'),
                          valor_bruto=round(round(decimal.Decimal(dado['Valor da venda']), 2), 2),
                          taxa=estabelecimento.taxa_credito,
                          valor_tarifa=round(
                              round(decimal.Decimal(dado['Valor da venda']) * bandeira.credito_moeda) / 100, 2),
                          valor_cobranca=round(round(decimal.Decimal(
                              dado['Valor da venda']) * estabelecimento.taxa_credito) / 100, 2),
                          valor_devido=round(round(decimal.Decimal(dado['Valor da venda'])) - round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_credito) / 100, 2),
                          lucro=round(round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_credito) / 100 - round(
                              decimal.Decimal(dado['Valor da venda']) * bandeira.credito_moeda) / 100, 2),
                          nr_maquina=dado['Número da máquina'],
                          cod_venda=dado['Código da venda'])
                list_vendas.append(v)
        else:
            if dado['Forma de pagamento'] == "Débito à vista":
                v = Venda(estabelecimento=estabelecimento,
                          tipo=dado['Forma de pagamento'],
                          bandeira=bandeira,
                          data_venda=pd.to_datetime(dado['Data da venda'], format='%d/%m/%Y %H:%M'),
                          previsao_pgto=pd.to_datetime(dado['Previsão de pagamento'], format='%d/%m/%Y'),
                          valor_bruto=round(round(decimal.Decimal(dado['Valor da venda']), 2), 2),
                          taxa=estabelecimento.taxa_debito,
                          valor_tarifa=round(
                              round(decimal.Decimal(dado['Valor da venda']) * bandeira.debito_vista) / 100, 2),
                          valor_cobranca=round(round(decimal.Decimal(
                              dado['Valor da venda']) * estabelecimento.taxa_debito) / 100, 2),
                          valor_devido=round(round(decimal.Decimal(dado['Valor da venda'])) - round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_debito) / 100, 2),
                          lucro=round(round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_debito) / 100 - round(
                              decimal.Decimal(dado['Valor da venda']) * bandeira.debito_vista) / 100, 2),
                          nr_maquina=dado['Número da máquina'],
                          cod_venda=dado['Código da venda'])
                list_vendas.append(v)
            else:
                v = Venda(estabelecimento=estabelecimento,
                          tipo=dado['Forma de pagamento'],
                          bandeira=bandeira,
                          data_venda=pd.to_datetime(dado['Data da venda'], format='%d/%m/%Y %H:%M'),
                          previsao_pgto=pd.to_datetime(dado['Previsão de pagamento'], format='%d/%m/%Y'),
                          valor_bruto=round(round(decimal.Decimal(dado['Valor da venda']), 2), 2),
                          taxa=estabelecimento.taxa_debito,
                          valor_tarifa=round(
                              round(decimal.Decimal(dado['Valor da venda']) * bandeira.debito_pre) / 100, 2),
                          valor_cobranca=round(round(decimal.Decimal(
                              dado['Valor da venda']) * estabelecimento.taxa_debito) / 100, 2),
                          valor_devido=round(round(decimal.Decimal(dado['Valor da venda'])) - round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_debito) / 100, 2),
                          lucro=round(round(
                              decimal.Decimal(dado['Valor da venda']) * estabelecimento.taxa_debito) / 100 - round(
                              decimal.Decimal(dado['Valor da venda']) * bandeira.debito_pre) / 100, 2),
                          nr_maquina=dado['Número da máquina'],
                          cod_venda=dado['Código da venda'])
                list_vendas.append(v)
    Venda.objects.bulk_create(list_vendas)
    for dado in d_records:
        venda = Venda.objects.get(cod_venda=dado['Código da venda'], valor_bruto=round(decimal.Decimal(dado['Valor da venda']), 2))
        if venda.valor_tarifa != round(decimal.Decimal(dado['Valor descontado']), 2):
            venda.contesta = True
            venda.valor_contestado = round(decimal.Decimal(dado['Valor descontado']), 2)
            venda.save()
    return redirect('machine:dashboardpendentes')

