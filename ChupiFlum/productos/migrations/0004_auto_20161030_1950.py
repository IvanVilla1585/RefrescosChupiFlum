# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-30 19:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_auto_20161030_1938'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productoterminado',
            options={'ordering': ('id',), 'permissions': (('form_view_producto', 'Formulario producto terminado'),)},
        ),
    ]
