from django.core.management.base import BaseCommand
from machine.views import teste_criar_dados


class Command(BaseCommand):
    help = 'Realização de teste para criar dados'

    def handle(self, *args, **kwargs):
        teste_criar_dados()
        self.stdout.write(self.style.SUCCESS('Teste realizado!'))

