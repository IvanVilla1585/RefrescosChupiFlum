# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from proveedores.models import Proveedore
from django.contrib.auth.models import User
from materiaprima.models import MateriaPrima
from estado_orden.models import EstadosOrdenes

class Pedido(models.Model):
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedore)
    usuario = models.ForeignKey(User)
    fecha = models.DateTimeField()
    total = models.DecimalField(decimal_places=3, max_digits=16)
    id_etado = models.ForeignKey(EstadosOrdenes)
    id_materia_prima = models.ManyToManyField(MateriaPrima, through='Detalle_Pedido', through_fields=('id_pedido', 'id_materia_prima'))

    def __str__(self):
        return '%s %s' % (self.usuario.first_name, self.fecha)

    class Meta:
        ordering = ('id',)
        db_table = 'pedidos'
        permissions = (
            ("form_view_pedido", u"Puede ver el formulario de pedidos"),
        )

class Detalle_Pedido(models.Model):
    id_pedido = models.ForeignKey(Pedido)
    id_materia_prima = models.ForeignKey(MateriaPrima)
    cantidad = models.DecimalField(decimal_places=3, max_digits=16)
    valor_unitario = models.DecimalField(decimal_places=3, max_digits=16)

    class Meta:
        ordering = ('id',)
        db_table='detalles_pedidos'
