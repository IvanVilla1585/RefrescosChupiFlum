# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-13 23:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_auto_20161213_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalles_formulas',
            name='cantidad_productos',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]