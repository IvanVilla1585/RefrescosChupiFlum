# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from materiaprima.models import MateriaPrima
from pedido.models import Pedido

class KardexMateriaPrima(models.Model):
    materiaprima = models.ForeignKey(MateriaPrima)
    pedido = models.ForeignKey(Pedido)
    fecha_movimiento = models.DateTimeField()
    entrada = models.BooleanField()
    salida = models.BooleanField()
    tipo_movimiento = models.BooleanField()
    cantidad = models.DecimalField(decimal_places=3, max_digits=16)
    valor_unitario = models.DecimalField(decimal_places=3, max_digits=16)
    total = models.DecimalField(decimal_places=3, max_digits=16)
    lote = models.CharField(max_length=30)
    fecha_vencimiento = models.DateTimeField()

    class Meta:
        ordering = ('id','fecha_vencimiento')
        db_table='kardex_materias_primas'
        permissions = (
            ("form_view_kardexmateriaprima", u"Formulario ejecución kardex materia prima"),
        )
