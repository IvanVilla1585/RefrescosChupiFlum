# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-01 19:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_auto_20171001_1056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalles_formulas',
            old_name='id_materia_prima',
            new_name='materia_prima',
        ),
        migrations.RenameField(
            model_name='detalles_formulas',
            old_name='id_producto',
            new_name='producto',
        ),
        migrations.RenameField(
            model_name='procesos_formulas',
            old_name='id_proceso',
            new_name='proceso',
        ),
        migrations.RenameField(
            model_name='procesos_formulas',
            old_name='id_producto',
            new_name='producto',
        ),
    ]
