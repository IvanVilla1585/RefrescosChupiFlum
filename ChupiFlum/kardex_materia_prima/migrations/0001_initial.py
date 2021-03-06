# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-09 14:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pedido', '0001_initial'),
        ('materiaprima', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KardexMateriaPrima',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_movimiento', models.DateTimeField()),
                ('entrada', models.BooleanField()),
                ('salida', models.BooleanField()),
                ('tipo_movimiento', models.BooleanField()),
                ('cantidad', models.DecimalField(decimal_places=3, max_digits=16)),
                ('valor_unitario', models.DecimalField(decimal_places=3, max_digits=16)),
                ('total', models.DecimalField(decimal_places=3, max_digits=16)),
                ('lote', models.CharField(max_length=30)),
                ('fecha_vencimiento', models.DateTimeField()),
                ('estado', models.BooleanField(default=True)),
                ('materiaprima', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaprima.MateriaPrima')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedido.Pedido')),
            ],
            options={
                'ordering': ('id', 'fecha_vencimiento'),
                'db_table': 'kardex_materias_primas',
                'permissions': (('form_view_kardexmateriaprima', 'Formulario ejecuci\xf3n kardex materia prima'),),
            },
        ),
    ]
