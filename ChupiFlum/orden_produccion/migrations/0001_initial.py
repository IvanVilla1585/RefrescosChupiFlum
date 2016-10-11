# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-08 00:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('estado_orden', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalle_Orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('id',),
                'db_table': 'detalles_ordenes_producion',
            },
        ),
        migrations.CreateModel(
            name='OrdenProduccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('fecha_elaboracion', models.DateTimeField()),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estado_orden.EstadosOrdenes')),
                ('id_producto', models.ManyToManyField(through='orden_produccion.Detalle_Orden', to='productos.ProductoTerminado')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
                'db_table': 'ordenes_produccion',
                'permissions': (('form_view_pedido', 'Puede ver el formulario de ordenes de producci\xf3n'),),
            },
        ),
        migrations.AddField(
            model_name='detalle_orden',
            name='id_orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orden_produccion.OrdenProduccion'),
        ),
        migrations.AddField(
            model_name='detalle_orden',
            name='id_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.ProductoTerminado'),
        ),
    ]
