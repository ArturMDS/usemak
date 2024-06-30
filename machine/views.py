import decimal
from django.shortcuts import render, reverse, redirect
from django.shortcuts import reverse
from django.db.models import Sum, F
from django.views.generic import (CreateView, \
    UpdateView, \
    TemplateView,
    FormView,
    ListView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (Venda,
                     Estabelecimento,
                     Usuario,
                     Bandeira,
                     Operadora,
                     Atualizacao)
from .forms import FormHomepage, CreateAtualizacaoForm
import pandas as pd
from datetime import datetime, timedelta, date
from .functions import inserir_dados


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

    def dispatch(self, request, *args, **kwargs):
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(em_conta=False)
        hoje = date.today()
        for venda in vendas:
            x = date(year=venda.previsao_pgto.year, month=venda.previsao_pgto.month, day=venda.previsao_pgto.day) - hoje
            if (x.days < 0) or venda.previsao_pgto == hoje:
                venda.em_conta = True
                venda.save()
        return super(Dashboardpendentes, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Dashboardpendentes, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).pendente().order_by('data_venda')
        context["vendas"] = vendas
        return context


class Dashboardcontestados(LoginRequiredMixin, TemplateView):
    template_name = "dashboardcontestados.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboardcontestados, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(contesta=True)
        context["vendas"] = vendas
        return context


class Dashboardprocessados(LoginRequiredMixin, TemplateView):
    template_name = "dashboardprocessados.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboardprocessados, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).processado()
        context["vendas"] = vendas
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


class PesquisaPendentes(ListView):
    template_name = "pesquisapendentes.html"
    model = Venda

    def get_queryset(self):
        inicio = self.request.GET.get('data_inicio')
        fim = self.request.GET.get('data_fim')
        usuario_logado = self.request.user
        if (len(inicio) == 10) and (len(fim) == 10):
            data_inicio = date(year=int(inicio[6:10]), month=int(inicio[3:5]), day=int(inicio[0:2]))
            data_fim = date(year=int(fim[6:10]), month=int(fim[3:5]), day=int(fim[0:2]))
            object_list = (Venda.objects.filter(estabelecimento__usuario=usuario_logado).pendente()
                           .filter(data_venda__gte=data_inicio).filter(data_venda__lte=data_fim).order_by('data_venda'))
            return object_list
        else:
            object_list = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(pago=False).filter(
                contesta=False).order_by('data_venda')
            return object_list

    def get_context_data(self, **kwargs):
        context = super(PesquisaPendentes, self).get_context_data(**kwargs)
        inicio = self.request.GET.get('data_inicio')
        fim = self.request.GET.get('data_fim')
        if (len(inicio) == 10) and (len(fim) == 10):
            context["inicio"] = inicio
            context["fim"] = fim
            return context
        else:
            msg = "Data inválida, digite no formato dd/mm/aaaa"
            context["msg"] = msg
            return context


def arquiva_pgto(request, id):
    venda = Venda.objects.get(id=id)
    venda.arquivado = True
    venda.save()
    return redirect('machine:dashboardprocessados')


def arquiva_pgto_todos(request):
    usuario_logado = request.user
    dia = int(request.GET.get('dia'))
    mes = int(request.GET.get('mes'))
    ano = int(request.GET.get('ano'))
    vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(previsao_pgto__day=dia).filter(
        previsao_pgto__month=mes).filter(previsao_pgto__year=ano).filter(pago=True)
    for venda in vendas:
        venda.arquivado = True
        venda.save()
    return redirect('machine:readvendas')


def cancela_pgto(request):
    usuario_logado = request.user
    dia = int(request.GET.get('dia'))
    mes = int(request.GET.get('mes'))
    ano = int(request.GET.get('ano'))
    vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(previsao_pgto__day=dia).filter(previsao_pgto__month=mes).filter(previsao_pgto__year=ano).filter(pago=True)
    for venda in vendas:
        venda.pago = False
        venda.save()
    return redirect('machine:readvendas')


class Readestabelecimento(LoginRequiredMixin, TemplateView):
    template_name = "readestabelecimento.html"

    def get_context_data(self, **kwargs):
        context = super(Readestabelecimento, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        clientes = self.request.user.estabelecimento.filter(usuario=usuario_logado)
        context['clientes'] = clientes
        return context


class Readvendas(LoginRequiredMixin, TemplateView):
    template_name = "readvendas.html"

    def get_context_data(self, **kwargs):
        context = super(Readvendas, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(pago=True).filter(arquivado=False).order_by('previsao_pgto')
        datas_set = {venda.previsao_pgto.toordinal() for venda in vendas}
        datas = [num for num in datas_set]
        datas.sort(reverse=True)
        vendas_query = [vendas.filter(previsao_pgto=date.fromordinal(data)) for data in datas]
        context['vendas'] = vendas
        context['vendas_query'] = vendas_query
        return context


class Createestabelecimento(LoginRequiredMixin, CreateView):
    template_name = "createestabelecimento.html"
    model = Estabelecimento
    fields = ['razao_social', 'codigo', 'taxa_debito', 'taxa_credito']

    def get_context_data(self, **kwargs):
        context = super(Createestabelecimento, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        clientes = self.request.user.estabelecimento.filter(usuario=usuario_logado)
        context['clientes'] = clientes
        return context

    def form_valid(self, form):
        usu = self.request.user
        form.instance.usuario = usu
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('machine:createestabelecimento')


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

    def get_success_url(self):
        return reverse('machine:readvendas')


class Createatualizacao(LoginRequiredMixin, CreateView):
    template_name = "createatualizacao.html"
    model = Atualizacao
    form_class = CreateAtualizacaoForm

    def get_form_kwargs(self):
        kwargs = super(Createatualizacao, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(Createatualizacao, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vigentes = Atualizacao.objects.filter(estabelecimento__usuario=usuario_logado).filter(vigente=True)
        context["vigentes"] = vigentes
        return context

    def get_success_url(self):
        return reverse('machine:createatualizacao')


class Updatevenda(LoginRequiredMixin, UpdateView):
    template_name = "updatevenda.html"
    model = Venda
    fields = ['estabelecimento', 'tipo',
              'bandeira', 'data_venda',
              'previsao_pgto', 'valor_bruto',
              'taxa', 'valor_tarifa', 'valor_cobranca',
              'valor_devido', 'lucro', 'valor_contestado']

    def get_success_url(self):
        return reverse('machine:readvendas')


class Updatecontestado(LoginRequiredMixin, UpdateView):
    template_name = "updatevenda.html"
    model = Venda
    fields = ['estabelecimento', 'tipo',
              'bandeira', 'data_venda',
              'previsao_pgto', 'valor_bruto',
              'taxa', 'valor_tarifa', 'valor_cobranca',
              'valor_devido', 'lucro', 'valor_contestado']

    def get_success_url(self):
        return reverse('machine:dashboardcontestados')


class Updateestabelecimento(LoginRequiredMixin, UpdateView):
    template_name = "updateestabelecimento.html"
    model = Estabelecimento
    fields = ['razao_social', 'codigo', 'taxa_debito', 'taxa_credito']

    def get_context_data(self, **kwargs):
        context = super(Updateestabelecimento, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        clientes = self.request.user.estabelecimento.filter(usuario=usuario_logado)
        context['clientes'] = clientes
        return context

    def get_success_url(self):
        return reverse('machine:readestabelecimentos')


def create_dados(request, id):
    atual = Atualizacao.objects.get(id=id)
    dataframe = pd.read_excel(atual.arquivo)
    dataframe = dataframe.drop([0, 1, 2], axis=0)
    dataframe.columns = dataframe.loc[3]
    dataframe = dataframe.drop([3], axis=0)
    dataframe = dataframe.drop(['Data da autorização da venda', 'Quantidade de parcelas', 'Resumo da operação', 'Taxas (%)',
                        'Tarifa', 'Número do cartão', 'Tipo de captura', 'Recebimento automático', 'Comissão mínima',
                        'Número da nota fiscal', 'Taxa de embarque', 'Valor da entrada', 'Valor do saque', 'Status',
                        'ID', 'Código de autorização', 'NSU'], axis=1)
    d_records = dataframe.to_dict("records")
    pk = atual.estabelecimento.id
    inserir_dados(request, d_records, pk)
    atual.vigente = False
    atual.delete()
    return redirect('machine:createatualizacao')

