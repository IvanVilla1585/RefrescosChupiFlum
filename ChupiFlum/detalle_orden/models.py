# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from orden_produccion.models import OrdenProduccion
from productos.models import ProductoTerminado

class Detalle_orden(models.Model):
    producto = models.ForeignKey(ProductoTerminado)
    orden_id = models.ForeignKey(OrdenProduccion)
    cantidad = models.PositiveIntegerField()

    class Meta:
        ordering = ('id',)
        db_table='detalles_ordenes_producion'
