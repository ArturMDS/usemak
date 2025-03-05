from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (Estabelecimento,
                     Venda,
                     Usuario,
                     Bandeira,
                     Operadora,
                     Atualizacao)

admin.site.register(Usuario, UserAdmin)
admin.site.register(Estabelecimento)
admin.site.register(Venda)
admin.site.register(Bandeira)
admin.site.register(Operadora)
admin.site.register(Atualizacao)

