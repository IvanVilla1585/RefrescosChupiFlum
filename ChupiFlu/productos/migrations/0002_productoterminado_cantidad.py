# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-28 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoterminado',
            name='cantidad',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
