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
    costo_produccion = models.DecimalField(decimal_places=2, max_digits=16, blank=True, default=0.0)
    precio_venta = models.DecimalField(decimal_places=2, max_digits=16, blank=True, default=0.0)
    cantidad = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    proceso = models.ManyToManyField(Proceso, through='Procesos_Formulas', through_fields=('producto', 'proceso'))
    estado = models.BooleanField(default=True, blank=True)
    materia_prima = models.ManyToManyField(MateriaPrima, through='Detalles_Formulas', through_fields=('producto', 'materia_prima'))


    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('id',)
        permissions = (
            ("form_view_producto", u"Formulario producto terminado"),
        )

class Detalles_Formulas(models.Model):
    producto = models.ForeignKey(ProductoTerminado)
    materia_prima = models.ForeignKey(MateriaPrima)
    cantidad = models.DecimalField(decimal_places=2, max_digits=16)

    def __str__(self):
        return self.id_producto.nombre

    class Meta:
        ordering = ('id',)
        db_table='detalles_formulas'

class Procesos_Formulas(models.Model):
    producto = models.ForeignKey(ProductoTerminado)
    proceso = models.ForeignKey(Proceso)

    def __str__(self):
        return self.id_producto.nombre

    class Meta:
        ordering = ('id',)
        db_table='procesos_formulas'

