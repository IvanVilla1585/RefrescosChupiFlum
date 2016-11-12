# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-09 14:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materiaprima', '0001_initial'),
        ('estado_orden', '0001_initial'),
        ('proveedores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalle_Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=3, max_digits=16)),
                ('valor_unitario', models.DecimalField(decimal_places=3, max_digits=16)),
                ('id_materia_prima', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaprima.MateriaPrima')),
            ],
            options={
                'ordering': ('id',),
                'db_table': 'detalles_pedidos',
                'permissions': (('form_view_pedido', 'Formulario pedido'),),
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=150, null=True)),
                ('fecha', models.DateTimeField()),
                ('total', models.DecimalField(decimal_places=3, max_digits=16)),
                ('id_etado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estado_orden.EstadosOrdenes')),
                ('id_materia_prima', models.ManyToManyField(through='pedido.Detalle_Pedido', to='materiaprima.MateriaPrima')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proveedores.Proveedore')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
                'db_table': 'pedidos',
            },
        ),
        migrations.AddField(
            model_name='detalle_pedido',
            name='id_pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedido.Pedido'),
        ),
    ]
