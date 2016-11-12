# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-10 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedore',
            name='correo_contacto',
            field=models.EmailField(blank=True, default='', max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='proveedore',
            name='correo_empresa',
            field=models.EmailField(blank=True, default='', max_length=254, null=True, unique=True),
        ),
    ]
