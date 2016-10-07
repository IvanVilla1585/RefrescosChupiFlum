# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from orden_produccion.models import OrdenProduccion
from productos.models import ProductoTerminado

class EjecucionOrden(models.Model):
    id_orden = models.ForeignKey(OrdenProduccion)
    id_producto = models.ForeignKey(ProductoTerminado)
    fecha = models.DateTimeField()
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return '%s %s' % (self.id_producto.nombre, self.fecha)

    class Meta:
        ordering = ('id',)
        db_table = 'ejecucion_ordenes'
        permissions = (
            ("form_view_ejecucion", u"Puede ver el formulario de ejecución ordenes de producción"),
        )
