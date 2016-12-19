# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from categorias.models import Categoria
from materiaprima.models import MateriaPrima
from proceso.models import Proceso
from presentaciones.models import Presentacion

class ProductoTerminado(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    categoria = models.ForeignKey(Categoria)
    presentacion = models.ForeignKey(Presentacion)
    costo_produccion = models.DecimalField(decimal_places=2, max_digits=16)
    precio_venta = models.DecimalField(decimal_places=2, max_digits=16)
    cantidad = models.PositiveIntegerField(default=True, blank=True)
    cantidad_productos = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    id_proceso = models.ManyToManyField(Proceso, db_table='procesos_productos')
    estado = models.BooleanField(default=True, blank=True)
    id_materia_prima = models.ManyToManyField(MateriaPrima, through='Detalles_Formulas', through_fields=('id_producto', 'id_materia_prima'))


    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('id',)
        permissions = (
            ("form_view_producto", u"Formulario producto terminado"),
        )

class Detalles_Formulas(models.Model):
    id_producto = models.ForeignKey(ProductoTerminado)
    id_materia_prima = models.ForeignKey(MateriaPrima)
    cantidad = models.DecimalField(decimal_places=2, max_digits=16)

    def __str__(self):
        return self.id_producto.nombre

    class Meta:
        ordering = ('id',)
        db_table='detalles_formulas'
