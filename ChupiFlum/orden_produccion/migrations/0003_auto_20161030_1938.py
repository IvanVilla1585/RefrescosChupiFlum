# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-30 19:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orden_produccion', '0002_auto_20161030_1849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordenproduccion',
            options={'ordering': ('id',), 'permissions': (('form_view_ordenproduccion', 'Formulario orden de producci\xf3n'), ('add_ordenproduccion', 'Insertar una orden de producci\xf3n'), ('change_ordenproduccion', 'Actualizar una orden de producci\xf3n'), ('delete_ordenproduccion', 'Eliminar una orden de producci\xf3n'))},
        ),
    ]
