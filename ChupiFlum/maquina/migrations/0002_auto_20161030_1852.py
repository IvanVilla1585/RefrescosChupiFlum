# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-30 18:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maquina', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='maquina',
            options={'ordering': ('id',)},
        ),
    ]
