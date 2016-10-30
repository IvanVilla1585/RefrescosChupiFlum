# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from productos.models import ProductoTerminado
from ejecucion_orden.models import EjecucionOrden

class KardexProductoTerminado(models.Model):
    producto_terminado = models.ForeignKey(ProductoTerminado)
    id_ejecucion = models.ForeignKey(EjecucionOrden)
    fecha_movimiento = models.DateTimeField()
    tipo_movimiento = models.BooleanField()
    cantidad = models.DecimalField(decimal_places=3, max_digits=16)
    valor_unitario = models.DecimalField(decimal_places=3, max_digits=16)
    total = models.DecimalField(decimal_places=3, max_digits=16)
    lote = models.CharField(max_length=30)
    fecha_vencimiento = models.DateTimeField()

    class Meta:
        ordering = ('id','fecha_vencimiento')
        db_table='kardex_productos_terminados'
        permissions = (
            ("form_view_kardexproductoterminado", u"Formulario ejecución kardex producto terminado"),
        )
