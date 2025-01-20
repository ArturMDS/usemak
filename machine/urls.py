from django.urls import path, re_path, reverse_lazy
from django.contrib.auth import views as auth_view
from .views import (confirma_pgto,
                    PesquisaPendentes,
                    arquiva_pgto,
                    arquiva_pgto_todos,
                    Dashboardpendentes,
                    Dashboardcontestados,
                    cancela_pgto,
                    Readestabelecimento,
                    Readvendas,
                    Createvenda,
                    Createestabelecimento,
                    Createatualizacao,
                    Updateestabelecimento,
                    Updatevenda,
                    Updatecontestado,
                    UpdateUsuario,
                    AcessoNegado,
                    create_dados,
                    ajusta_contestados,
                    PesquisaPdf,
                    limpa_arquivo)


app_name = 'machine'

urlpatterns = [
    path('login', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_view.LogoutView.as_view(template_name='login.html'), name='logout'),
    path("change-password/", auth_view.PasswordChangeView.as_view(success_url=reverse_lazy('machine:changedone'),
                                                                  template_name="change-password.html"),
         name='changepassword'),
    path("change-done/", auth_view.PasswordChangeDoneView.as_view(template_name="change-done.html"), name='changedone'),
    path('contestados', Dashboardcontestados.as_view(), name='dashboardcontestados'),
    path('pendentes', Dashboardpendentes.as_view(), name='dashboardpendentes'),
    path('pendentes/pesquisa', PesquisaPendentes.as_view(), name='pesquisapendentes'),
    path('pendentes/pesquisa/pdf', PesquisaPdf.as_view(), name='pesquisa_pdf'),
    path('read/estabelecimento', Readestabelecimento.as_view(), name='readestabelecimentos'),
    path('read/vendas', Readvendas.as_view(), name='readvendas'),
    path('create/venda', Createvenda.as_view(), name='createvenda'),
    path('create/estabelecimento', Createestabelecimento.as_view(), name='createestabelecimento'),
    path('create/atualizacao', Createatualizacao.as_view(), name='createatualizacao'),
    path('update/venda/<int:pk>', Updatevenda.as_view(), name='updatevenda'),
    path('update/contestado/<int:pk>', Updatecontestado.as_view(), name='updatecontestado'),
    path('update/estabelecimento/<int:pk>', Updateestabelecimento.as_view(), name='updateestabelecimento'),
    path('update/usuario/<int:pk>', UpdateUsuario.as_view(), name='updateusuario'),
    path('acessonegado', AcessoNegado.as_view(), name='acessonegado'),
    re_path(r'^create_dados/(?P<id>\d+)/$', create_dados, name='create_dados'),
    re_path(r'^ajusta_contestados/(?P<id>\d+)/$', ajusta_contestados, name='ajusta_contestados'),
    re_path(r'^confirma_pgto/(?P<id>\d+)/$', confirma_pgto, name='confirma_pgto'),
    re_path(r'^arquiva_pgto_todos/$', arquiva_pgto_todos, name='arquiva_pgto_todos'),
    path('arquiva_pgto', arquiva_pgto, name='arquiva_pgto'),
    re_path(r'^cancela_pgto/$', cancela_pgto, name='cancela_pgto'),
    re_path(r'^limpa_arquivo/$', limpa_arquivo, name='limpa_arquivo'),
]

#TODO: proposta para apagar >> contestados
