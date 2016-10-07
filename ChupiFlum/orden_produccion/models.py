# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from estado_orden.models import EstadosOrdenes
from productos.models import ProductoTerminado

class OrdenProduccion(models.Model):
    usuario = models.ForeignKey(User)
    fecha = models.DateTimeField()
    fecha_elaboracion = models.DateTimeField()
    estado = models.ForeignKey(EstadosOrdenes)
    id_producto = models.ManyToManyField(ProductoTerminado, through='Detalle_Orden', through_fields=('id_orden', 'id_producto'))

    def __str__(self):
        return '%s %s' % (self.usuario.first_name, self.estado)

    class Meta:
        ordering = ('id',)
        db_table = 'ordenes_produccion'
        permissions = (
            ("form_view_pedido", u"Puede ver el formulario de ordenes de producción"),
        )

class Detalle_Orden(models.Model):
    id_orden = models.ForeignKey(OrdenProduccion)
    id_producto = models.ForeignKey(ProductoTerminado)
    cantidad = models.PositiveIntegerField()

    class Meta:
        ordering = ('id',)
        db_table='detalles_ordenes_producion'
