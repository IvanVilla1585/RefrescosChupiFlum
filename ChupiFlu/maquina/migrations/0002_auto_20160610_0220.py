# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-10 02:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maquina', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='maquina',
            options={'ordering': ('id',), 'permissions': (('form_view_maquina', 'M\xf3dulo Maquinas'),)},
        ),
    ]
