# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-05 08:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0002_auto_20160514_1524'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proveedore',
            options={'ordering': ('id',), 'permissions': (('form_view_proveedor', 'puede ver el formulario'),)},
        ),
    ]
