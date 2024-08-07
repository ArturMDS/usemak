# Generated by Django 3.2.23 on 2024-08-07 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0007_auto_20240623_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='nr_maquina',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='venda',
            name='tipo',
            field=models.CharField(choices=[('Débito à vista', 'Débito à vista'), ('Débito pré-pago', 'Débito pré-pago'), ('Crédito à vista', 'Crédito à vista'), ('Crédito pré-pago', 'Crédito pré-pago'), ('Crédito conversor moeda', 'Crédito conversor moeda'), ('Crédito parcelado loja 2x', 'Crédito parcelado loja 2x'), ('Crédito parcelado loja 3x', 'Crédito parcelado loja 3x'), ('Crédito parcelado loja 4x', 'Crédito parcelado loja 4x'), ('Crédito parcelado loja 5x', 'Crédito parcelado loja 5x'), ('Crédito parcelado loja 6x', 'Crédito parcelado loja 6x'), ('Crédito parcelado loja 7x', 'Crédito parcelado loja 7x'), ('Crédito parcelado loja 8x', 'Crédito parcelado loja 8x'), ('Crédito parcelado loja 9x', 'Crédito parcelado loja 9x'), ('Crédito parcelado loja 10x', 'Crédito parcelado loja 10x'), ('Crédito parcelado loja 11x', 'Crédito parcelado loja 11x'), ('Crédito parcelado loja 12x', 'Crédito parcelado loja 12x')], default='Crédito à vista', max_length=50),
        ),
    ]
