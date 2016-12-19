# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from materiaprima.models import MateriaPrima
from pedido.models import Pedido

class KardexMateriaPrima(models.Model):
    materiaprima = models.ForeignKey(MateriaPrima)
    pedido = models.ForeignKey(Pedido)
    fecha_movimiento = models.DateTimeField()
    entrada = models.BooleanField(default=False, blank=True)
    salida = models.BooleanField(default=False, blank=True)
    cantidad = models.DecimalField(decimal_places=2, max_digits=16)
    total = models.DecimalField(decimal_places=2, max_digits=16)
    lote = models.CharField(max_length=30)
    fecha_vencimiento = models.DateTimeField()
    estado = models.BooleanField(default=True, blank=True)

    class Meta:
        ordering = ('id','fecha_vencimiento')
        db_table='kardex_materias_primas'
        permissions = (
            ("form_view_kardexmateriaprima", u"Formulario ejecución kardex materia prima"),
        )
