# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from unidadesmedida.models import UnidadMedida

class Maquina(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    capacidad = models.DecimalField(decimal_places=3, max_digits=16)
    unidad_medida = models.ForeignKey(UnidadMedida)
    tiempo = models.TimeField(max_length=15)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('id',)
        db_table = 'maquinas'
        permissions = (
            ("form_view_maquina", u"Formulario maquina"),
        )
