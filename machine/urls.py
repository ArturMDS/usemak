from django.urls import path, re_path
from django.contrib.auth import views as auth_view
from .views import (confirma_pgto,
                    arquiva_pgto,
                    Dashboardpendentes,
                    Dashboardprocessados,
                    Dashboardcontestados,
                    cancela_pgto,
                    Readestabelecimento,
                    Readvendas,
                    Createvenda,
                    Createestabelecimento,
                    Updateestabelecimento,
                    Updatevenda,
                    Updatecontestado,
                    AcessoNegado,
                    create_dados,
                    ajusta_contestados)


app_name = 'machine'

urlpatterns = [
    path('login', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_view.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('processados', Dashboardprocessados.as_view(), name='dashboardprocessados'),
    path('contestados', Dashboardcontestados.as_view(), name='dashboardcontestados'),
    path('pendentes', Dashboardpendentes.as_view(), name='dashboardpendentes'),
    path('read/estabelecimento', Readestabelecimento.as_view(), name='readestabelecimentos'),
    path('read/vendas', Readvendas.as_view(), name='readvendas'),
    path('create/venda', Createvenda.as_view(), name='createvenda'),
    path('create/estabelecimento', Createestabelecimento.as_view(), name='createestabelecimento'),
    path('update/venda/<int:pk>', Updatevenda.as_view(), name='updatevenda'),
    path('update/contestado/<int:pk>', Updatecontestado.as_view(), name='updatecontestado'),
    path('update/estabelecimento/<int:pk>', Updateestabelecimento.as_view(), name='updateestabelecimento'),
    path('acessonegado', AcessoNegado.as_view(), name='acessonegado'),
    path('create_dados', create_dados, name='create_dados'),
    re_path(r'^ajusta_contestados/(?P<id>\d+)/$', ajusta_contestados, name='ajusta_contestados'),
    re_path(r'^confirma_pgto/(?P<id>\d+)/$', confirma_pgto, name='confirma_pgto'),
    re_path(r'^arquiva_pgto/(?P<id>\d+)/$', arquiva_pgto, name='arquiva_pgto'),
    re_path(r'^cancela_pgto/(?P<id>\d+)/$', cancela_pgto, name='cancela_pgto'),
]
