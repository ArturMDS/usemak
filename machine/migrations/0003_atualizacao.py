# Generated by Django 3.2.23 on 2024-06-07 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0002_auto_20240604_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atualizacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicio', models.DateField(verbose_name='Primeiro dia da atualização')),
                ('data_fim', models.DateField(verbose_name='Último dia da atualização')),
                ('nome', models.CharField(max_length=50)),
                ('vigente', models.BooleanField(default=True)),
                ('arquivo', models.FileField(upload_to='arquivos')),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atualizacao', to='machine.estabelecimento')),
            ],
        ),
    ]
