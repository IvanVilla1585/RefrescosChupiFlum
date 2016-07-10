# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from unidadesmedida.models import UnidadesMateriaPrima
from categoriasmateriaprima.models import CategoriaMateriaPrima

class MateriaPrima(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    unidad_medida = models.ForeignKey(UnidadesMateriaPrima)
    categoria = models.ForeignKey(CategoriaMateriaPrima)
    cantidad = models.FloatField()
    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('id',)
        permissions = (
            ("form_view_materiaprima", u"Módulo Materia Prima"),
        )
