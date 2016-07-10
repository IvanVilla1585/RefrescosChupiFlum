# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from unidadesmedida.models import UnidadesMateriaPrima

class Maquina(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    capacidad = models.FloatField()
    unidad_medida = models.ForeignKey(UnidadesMateriaPrima)
    tiempo = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('id',)
        permissions = (
            ("form_view_maquina", u"Módulo Maquinas"),
        )
