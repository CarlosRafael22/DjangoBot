# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 13:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log_Peso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('data', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Log_Refeicao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refeicao_nome', models.CharField(max_length=100, null=True)),
                ('descricao_refeicao', models.CharField(max_length=500)),
                ('data', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_chat_id', models.CharField(max_length=50)),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='log_refeicao',
            name='participante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Participante'),
        ),
        migrations.AddField(
            model_name='log_peso',
            name='participante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Participante'),
        ),
    ]
