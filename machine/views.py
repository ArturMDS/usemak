import decimal
from django.shortcuts import render, reverse, redirect, resolve_url
from django.db.models import Sum, F
from django.contrib import messages
from django.views.generic import (CreateView, \
    UpdateView, \
    TemplateView,
    FormView,
    ListView,
    View)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import (Venda,
                     Estabelecimento,
                     Usuario,
                     Bandeira,
                     Operadora,
                     Atualizacao)
from .forms import FormHomepage, CreateAtualizacaoForm
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
from datetime import datetime, timedelta, date
from .functions import inserir_dados_cielo, inserir_dados_cpay
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import io
import random


class Render:
    @staticmethod
    def render(path: str, params: dict, filename: str):
        template = get_template(path)
        html = template.render(params)
        response = io.BytesIO()
        pdf = pisa.pisaDocument(
            io.BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(
                response.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)


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
        total_vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).pendente().order_by('data_venda')
        querys = {}
        num = 0
        for estab in Estabelecimento.objects.filter(usuario=usuario_logado):
            querys[f"vendas{num}"] = total_vendas.filter(estabelecimento=estab)
            num += 1
        operadoras = Operadora.objects.all()
        estabelecimentos = querys.values()
        context["usuario_logado"] = usuario_logado
        context["total_vendas"] = total_vendas
        context["estabelecimentos"] = estabelecimentos
        context["operadoras"] = operadoras
        return context


class Dashboardcontestados(LoginRequiredMixin, TemplateView):
    template_name = "dashboardcontestados.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboardcontestados, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(contesta=True)
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

    def get_queryset(self, *args):
        if self.request.GET.get('data_inicio'):
            inicio = self.request.GET.get('data_inicio')
            fim = self.request.GET.get('data_fim')
            self.request.session['data_inicio'] = inicio
            self.request.session['data_fim'] = fim
            usuario_logado = self.request.user
            operadora = self.request.GET.get('operadora')
            if (len(inicio) == 10) and (len(fim) == 10):
                data_inicio = date(year=int(inicio[6:10]), month=int(inicio[3:5]), day=int(inicio[0:2]))
                data_fim = date(year=int(fim[6:10]), month=int(fim[3:5]), day=int(fim[0:2]))
                object_list = (Venda.objects.filter(estabelecimento__usuario=usuario_logado).pendente()
                               .filter(data_venda__range=(data_inicio, data_fim))
                               .filter(bandeira__operadora__nome=operadora).order_by('data_venda'))
                return object_list
            else:
                object_list = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(pago=False).filter(
                    contesta=False).filter(bandeira__operadora__nome=operadora).order_by('data_venda')
                return object_list
        else:
            inicio = self.request.session.get('data_inicio')
            fim = self.request.session.get('data_fim')
            operadora = self.request.GET.get('operadora')
            usuario_logado = self.request.user
            if (len(inicio) == 10) and (len(fim) == 10):
                data_inicio = date(year=int(inicio[6:10]), month=int(inicio[3:5]), day=int(inicio[0:2]))
                data_fim = date(year=int(fim[6:10]), month=int(fim[3:5]), day=int(fim[0:2]))
                object_list = (Venda.objects.filter(estabelecimento__usuario=usuario_logado).pendente()
                               .filter(data_venda__range=(data_inicio, data_fim))
                               .filter(bandeira__operadora__nome=operadora).order_by('data_venda'))
                return object_list
            else:
                object_list = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(pago=False).filter(
                    contesta=False).filter(bandeira__operadora__nome=operadora).order_by('data_venda')
                return object_list

    def get_context_data(self, **kwargs):
        context = super(PesquisaPendentes, self).get_context_data(**kwargs)
        if self.request.GET.get('data_inicio'):
            inicio = self.request.GET.get('data_inicio')
            fim = self.request.GET.get('data_fim')
        else:
            inicio = self.request.session.get('data_inicio')
            fim = self.request.session.get('data_fim')
        usuario_logado = self.request.user
        operadora = self.request.GET.get('operadora')
        if (len(inicio) == 10) and (len(fim) == 10):
            data_inicio = date(year=int(inicio[6:10]), month=int(inicio[3:5]), day=int(inicio[0:2]))
            data_fim1 = date(year=int(fim[6:10]), month=int(fim[3:5]), day=int(fim[0:2]))
            d = timedelta(seconds=60*60*24)
            data_fim = data_fim1 + d
            total_vendas = (Venda.objects.filter(estabelecimento__usuario=usuario_logado).pendente()
                            .filter(data_venda__range=(data_inicio, data_fim))
                            .filter(bandeira__operadora__nome=operadora).order_by('data_venda'))
        else:
            total_vendas = (Venda.objects.filter(estabelecimento__usuario=usuario_logado)
                            .filter(bandeira__operadora__nome=operadora)
                            .filter(pago=False).filter(contesta=False).order_by('data_venda'))
        querys = {}
        num = 0
        for estab in Estabelecimento.objects.filter(usuario=usuario_logado):
            querys[f"vendas{num}"] = total_vendas.filter(estabelecimento=estab)
            num += 1
        estabelecimentos = querys.values()
        context["total_vendas"] = total_vendas
        context["operadora"] = operadora
        context["estabelecimentos"] = estabelecimentos
        if (len(inicio) == 10) and (len(fim) == 10):
            context["inicio"] = inicio
            context["fim"] = fim
        else:
            messages.warning(self.request, "Data inválida, digite no formato dd/mm/aaaa")
        return context


def arquiva_pgto(request):
    usuario_logado = request.user
    dia = int(request.GET.get('dia'))
    mes = int(request.GET.get('mes'))
    ano = int(request.GET.get('ano'))
    vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(previsao_pgto__day=dia).filter(
        previsao_pgto__month=mes).filter(previsao_pgto__year=ano).filter(pago=True)
    for venda in vendas:
        venda.arquivado = True
        venda.save()
    messages.success(request, "Vendas arquivadas com sucesso!")
    return redirect('machine:readvendas')


def arquiva_pgto_todos(request):
    usuario_logado = request.user
    if request.GET.get('data_inicio') and request.GET.get('data_fim'):
        inicio = request.GET.get('data_inicio')
        fim = request.GET.get('data_fim')
        data_inicio = date(year=int(inicio[6:10]), month=int(inicio[3:5]), day=int(inicio[0:2]))
        data_fim1 = date(year=int(fim[6:10]), month=int(fim[3:5]), day=int(fim[0:2]))
        d = timedelta(seconds=60 * 60 * 24)
        data_fim = data_fim1 + d
        tipo = request.GET.get('tipo')
        estabelecimento = request.GET.get('estabelecimento')
        if tipo == "Débito":
            vendas = (Venda.objects.filter(estabelecimento__usuario=usuario_logado).debito()
                      .pendente().filter(data_venda__gte=data_inicio)
                      .filter(data_venda__lte=data_fim).filter(estabelecimento__razao_social=estabelecimento))
        else:
            vendas = (Venda.objects.filter(estabelecimento__usuario=usuario_logado).credito()
                      .pendente().filter(data_venda__gte=data_inicio).filter(data_venda__lte=data_fim)
                      .filter(estabelecimento__razao_social=estabelecimento))
        for venda in vendas:
            venda.pago = True
            venda.save()
        messages.success(request, f"Vendas do {estabelecimento} arquivadas com sucesso!")
        return redirect('machine:pesquisapendentes')
    else:
        tipo = request.GET.get('tipo')
        estabelecimento = request.GET.get('estabelecimento')
        if tipo == "Débito":
            vendas = (Venda.objects.filter(estabelecimento__usuario=usuario_logado)
                      .filter(estabelecimento__razao_social=estabelecimento).debito().pendente())
        else:
            vendas = (Venda.objects.filter(estabelecimento__usuario=usuario_logado)
                      .filter(estabelecimento__razao_social=estabelecimento).credito().pendente())
        for venda in vendas:
            venda.pago = True
            venda.save()
        messages.success(request, f"Vendas do {estabelecimento} arquivadas com sucesso!")
        if request.GET.get('data_inicio'):
            return redirect('machine:pesquisapendentes')
        else:
            return redirect('machine:dashboardpendentes')


def cancela_pgto(request):
    usuario_logado = request.user
    dia = int(request.GET.get('dia'))
    mes = int(request.GET.get('mes'))
    ano = int(request.GET.get('ano'))
    vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(previsao_pgto__day=dia).filter(previsao_pgto__month=mes).filter(previsao_pgto__year=ano).filter(pago=True)
    for venda in vendas:
        venda.pago = False
        venda.save()
    messages.success(request, "Vendas desarquivadas, consulte os Pendentes!")
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


class Createestabelecimento(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = "createestabelecimento.html"
    model = Estabelecimento
    fields = ['razao_social', 'codigo', 'taxa_debito', 'taxa_credito']
    success_message = "%(razao_social)s criado com sucesso!"

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


class Createvenda(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = "createvenda.html"
    model = Venda
    fields = ['estabelecimento', 'tipo',
              'bandeira', 'data_venda',
              'previsao_pgto', 'valor_bruto',
              'nr_maquina', 'cod_venda']
    success_message = "Venda criada com sucesso!"

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
        atual = Atualizacao.objects.last()
        if str(atual.arquivo)[-4:] == "xlsx":
            messages.success(self.request, "Arquivo no formato correto e salvo com sucesso!")
        elif str(atual.arquivo)[-3:] == "xls":
            messages.success(self.request, "Arquivo no formato correto e salvo com sucesso!")
        else:
            messages.warning(self.request, "Arquivo no formato incorreto, NÃO SALVO!")
            atual.delete()
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


class UpdateUsuario(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = "updateusuario.html"
    model = Usuario
    fields = ['username', 'email']
    success_message = "%(username)s atualizado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(UpdateUsuario, self).get_context_data(**kwargs)
        usuario_logado = self.request.user
        clientes = self.request.user.estabelecimento.filter(usuario=usuario_logado)
        context['clientes'] = clientes
        return context

    def get_success_url(self):
        return reverse('machine:dashboardpendentes')


def create_dados(request, id):
    atual = Atualizacao.objects.get(id=id)
    try:
        dataframe = pd.read_excel(atual.arquivo)
    except:
        messages.warning(request, "Não foi possível abrir o arquivo")
        return redirect('machine:createatualizacao')
    num = 0
    m = 0
    operadora = ''
    list = []
    try:
        while num == 0:
            for dado in dataframe.iloc[m]:
                if "Hora" in str(dado):
                    num = 1
            list.append(m)
            m += 1
        list.pop(list[-1])
        num = 0
        m = 0
        while num == 0:
            for dado in dataframe.iloc[m]:
                if "C6Pay" in str(dado):
                    num = 1
                    operadora = 'C6Pay'
                    break
                elif "Cielo" in str(dado):
                    num = 1
                    operadora = 'Cielo'
                    break
            m += 1
    except:
        messages.warning(request, "Erro na leitura do arquivo")
        return redirect('machine:createatualizacao')
    if operadora == 'Cielo':
        try:
            dataframe = dataframe.drop(list, axis=0)
            dataframe.columns = dataframe.loc[8]
            dataframe = dataframe.drop([8], axis=0)
            d_records = dataframe.to_dict("records")
            pk = atual.estabelecimento.id
        except:
            messages.warning(request, "Erro na formatação do dataframe")
            return redirect('machine:createatualizacao')
        try:
            inserir_dados_cielo(request, d_records, pk, operadora)
        except:
            messages.warning(request, "Não foi possível inserir dados no banco de dados")
            return redirect('machine:createatualizacao')
        atual.vigente = False
        atual.delete()
        messages.success(request, "Banco de dados atualizado com sucesso!")
    elif operadora == 'C6Pay':
        try:
            dataframe = dataframe.drop(list, axis=0)
            dataframe.columns = dataframe.loc[2]
            dataframe = dataframe.drop([2], axis=0)
            dataframe = dataframe[dataframe['Status da venda'] != 'Recusada']
            dataframe = dataframe[dataframe['Status da venda'] != 'Devolvida']
            dataframe = dataframe[dataframe['Tipo de operação'] != 'Pix']
        except:
            messages.warning(request, "Erro na formatação do dataframe")
            return redirect('machine:createatualizacao')
        d_records = dataframe.to_dict("records")
        pk = atual.estabelecimento.id
        try:
            inserir_dados_cpay(request, d_records, pk, operadora)
        except:
            messages.warning(request, "Não foi possível inserir dados no banco de dados")
            return redirect('machine:createatualizacao')
        atual.vigente = False
        atual.delete()
        messages.success(request, "Banco de dados atualizado com sucesso!")
    return redirect('machine:createatualizacao')


class PesquisaPdf(View):

    def get(self, request, *args, **kwargs):
        if request.GET.get('data_inicio') and request.GET.get('data_fim'):
            inicio = request.GET.get('data_inicio')
            fim = request.GET.get('data_fim')
            data_inicio = date(year=int(inicio[6:10]), month=int(inicio[3:5]), day=int(inicio[0:2]))
            data_fim1 = date(year=int(fim[6:10]), month=int(fim[3:5]), day=int(fim[0:2]))
            d = timedelta(seconds=60 * 60 * 24)
            data_fim = data_fim1 + d
            estabelecimento = request.GET.get('estabelecimento')
            usuario_logado = self.request.user
            operadora = request.GET.get('operadora')
            vendas = (Venda.objects.filter(estabelecimento__usuario=usuario_logado)
                      .filter(estabelecimento__razao_social=estabelecimento)
                      .filter(bandeira__operadora__nome=operadora).pendente()
                      .filter(data_venda__range=(data_inicio, data_fim)).order_by('data_venda'))

        params = {
            'operadora': operadora,
            'vendas': vendas,
            'estabelecimento': estabelecimento,
            'data_inicio': inicio,
            'data_fim': fim,
            'request': request,
        }
        return Render.render('pesquisa_pdf.html',
                             params,
                             f'{operadora} - {estabelecimento} - {data_inicio.strftime("%d-%m")} a {data_fim1.strftime("%d-%m")}')


class PesquisaDetalhadaPdf(View):

    def get(self, request, *args, **kwargs):
        if request.GET.get('data_inicio') and request.GET.get('data_fim'):
            inicio = request.GET.get('data_inicio')
            fim = request.GET.get('data_fim')
            data_inicio = date(year=int(inicio[6:10]), month=int(inicio[3:5]), day=int(inicio[0:2]))
            data_fim1 = date(year=int(fim[6:10]), month=int(fim[3:5]), day=int(fim[0:2]))
            d = timedelta(seconds=60 * 60 * 24)
            data_fim = data_fim1 + d
            vendas_dia = []
            usuario_logado = self.request.user
            operadora = request.GET.get('operadora')
            estabelecimento = request.GET.get('estabelecimento')
            num = data_fim.day - data_inicio.day
            while num != 0:
                dia = data_fim.day - num
                data = date(year=int(inicio[6:10]), month=int(inicio[3:5]), day=dia)
                vendas_dia.append(Venda.objects.filter(estabelecimento__usuario=usuario_logado)
                                  .filter(estabelecimento__razao_social=estabelecimento)
                                  .filter(bandeira__operadora__nome=operadora).pendente()
                                  .filter(data_venda__date=data))
                num -= 1
        params = {
            'operadora': operadora,
            'vendas_dia': vendas_dia,
            'estabelecimento': estabelecimento,
            'data_inicio': inicio,
            'data_fim': fim,
            'request': request,
        }
        return Render.render('pesquisa_detalhada_pdf.html',
                             params,
                             f'{operadora} - {estabelecimento} - Detalhado {data_inicio.strftime("%d-%m")} a {data_fim1.strftime("%d-%m")}')


def limpa_arquivo(request):
    usuario_logado = request.user
    vendas = Venda.objects.filter(estabelecimento__usuario=usuario_logado).filter(arquivado=True)
    vendas.delete()
    messages.success(request, f"Todas as vendas do arquivo foram deletadas com sucesso!")
    return redirect('machine:readvendas')


def enviar_email(assunto, msg):
    send_mail(
        assunto,
        msg,
        settings.EMAIL_HOST_USER,
        ["arturmds@yahoo.com.br"],
        fail_silently=False,
    )


def teste_criar_dados():
    a = random.randint(1, 2)
    if a == 1:
        dataframe = pd.read_excel(r"static/files/c6pay.xlsx")
        msg = "Teste C6Pay"
    else:
        dataframe = pd.read_excel(r"static/files/cielo.xlsx")
        msg = "Teste Cielo"
    num = 0
    m = 0
    operadora = ''
    list = []
    try:
        while num == 0:
            for dado in dataframe.iloc[m]:
                if "Hora" in str(dado):
                    num = 1
            list.append(m)
            m += 1
        list.pop(list[-1])
    except:
        msg += "\n Erro na leitura da coluna"
    num = 0
    m = 0
    try:
        while num == 0:
            for dado in dataframe.iloc[m]:
                if "C6Pay" in str(dado):
                    num = 1
                    operadora = 'C6Pay'
                    break
                elif "Cielo" in str(dado):
                    num = 1
                    operadora = 'Cielo'
                    break
            m += 1
    except:
        msg += "\n Erro na leitura da coluna do arquivo"
    if operadora == 'Cielo':
        try:
            dataframe = dataframe.drop(list, axis=0)
            dataframe.columns = dataframe.loc[8]
            dataframe = dataframe.drop([8], axis=0)
        except:
            msg += "\n Erro na formatação do arquivo"
    elif operadora == 'C6Pay':
        try:
            dataframe = dataframe.drop(list, axis=0)
            dataframe.columns = dataframe.loc[2]
            dataframe = dataframe.drop([2], axis=0)
            dataframe = dataframe[dataframe['Status da venda'] != 'Recusada']
            dataframe = dataframe[dataframe['Status da venda'] != 'Devolvida']
            dataframe = dataframe[dataframe['Tipo de operação'] != 'Pix']
        except:
            msg += "\n Erro na formatação do arquivo"
    assunto = "USEMAK - Teste de criação de dados"
    if msg == "Teste C6Pay" or msg == "Teste Cielo":
        msg += "\n\nTestes finalizados sem alterações!"
    else:
        msg += "\n\n Testes finalizados"
    enviar_email(assunto, msg)

