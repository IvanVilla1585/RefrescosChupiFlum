# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from materiaprima.models import MateriaPrima
from pedido.models import Pedido

class Detalle_Pedido(models.Model):
    materiaprima = models.ForeignKey(MateriaPrima)
    pedido = models.ForeignKey(Pedido)
    cantidad = models.DecimalField(decimal_places=3, max_digits=16)
    valor_unitario = models.DecimalField(decimal_places=3, max_digits=16)

    class Meta:
        ordering = ('id',)
        db_table='detalles_pedidos'
