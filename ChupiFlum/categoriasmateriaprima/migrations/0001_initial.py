# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-30 16:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaMateriaPrima',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ('id',),
                'db_table': 'categorias_materias_primas',
            },
        ),
    ]
