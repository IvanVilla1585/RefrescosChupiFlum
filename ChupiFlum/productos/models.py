# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from categorias.models import Categoria
from materiaprima.models import MateriaPrima
from proceso.models import Proceso

class ProductoTerminado(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    categoria = models.ForeignKey(Categoria)
    costo_produccion = models.DecimalField(decimal_places=2, max_digits=16)
    precio_venta = models.DecimalField(decimal_places=2, max_digits=16)
    cantidad = models.PositiveIntegerField(default=0)
    id_detalle_formula = models.ManyToManyField(MateriaPrima, db_table='detalles_formulas')
    id_proceso = models.ManyToManyField(Proceso, db_table='procesos_productos')
    estado = models.BooleanField(default=True, blank=True)


    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('id',)
        permissions = (
            ("form_view_producto", u"Formulario producto terminado"),
        )
