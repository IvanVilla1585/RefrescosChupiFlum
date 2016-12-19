# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-07 02:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit', models.CharField(max_length=20, unique=True)),
                ('empresa', models.CharField(max_length=120)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('fax', models.CharField(blank=True, max_length=15, null=True)),
                ('correo_empresa', models.EmailField(blank=True, max_length=254, null=True)),
                ('nombre_contacto', models.CharField(max_length=50)),
                ('apellido_contacto', models.CharField(blank=True, max_length=50, null=True)),
                ('telefono_contacto', models.CharField(max_length=15)),
                ('correo_contacto', models.EmailField(blank=True, max_length=254, null=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('id',),
                'db_table': 'proveedores',
                'permissions': (('form_view_proveedore', 'Formulario proveedor'),),
            },
        ),
    ]
