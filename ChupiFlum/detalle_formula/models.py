# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from productos.models import ProductoTerminado
from materiaprima.models import MateriaPrima

class Detalle_formula(models.Model):
    id_materia_prima = models.ForeignKey(MateriaPrima)
    id_producto = models.ForeignKey(ProductoTerminado)
    cantidad = models.PositiveIntegerField()

    class Meta:
        ordering = ('id',)
        db_table='detalles_formular'
