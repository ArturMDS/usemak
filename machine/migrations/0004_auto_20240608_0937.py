# Generated by Django 3.2.23 on 2024-06-08 12:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0003_atualizacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='previsao_pgto',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Previsão de pagamento'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='taxa',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Sua taxa'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='valor_bruto',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Valor da venda'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='valor_cobranca',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Valor a ser cobrado'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='valor_contestado',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Valor cobrado pela operadora'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='valor_devido',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Valor devido ao cliente'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='valor_tarifa',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Valor da tarifa da operadora'),
        ),
    ]
