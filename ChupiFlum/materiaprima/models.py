# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from unidadesmedida.models import UnidadMedida
from categoriasmateriaprima.models import CategoriaMateriaPrima

class MateriaPrima(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    unidad_medida = models.ForeignKey(UnidadMedida)
    categoria = models.ForeignKey(CategoriaMateriaPrima)
    cantidad = models.DecimalField(decimal_places=2, max_digits=16, default=0, null=True, blank=True)
    stock = models.DecimalField(decimal_places=2, max_digits=16)
    estado = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('id',)
        db_table = 'materiasprimas'
        permissions = (
            ("form_view_materiaprima", u"Formulario materia prima"),
        )
