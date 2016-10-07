# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from unidadesmedida.models import UnidadMedida
from maquina.models import Maquina

class Proceso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    maquina = models.ForeignKey(Maquina)
    tiempo = models.TimeField()
    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('id',)
        db_table = 'procesos'
        permissions = (
            ("form_view_materiaprima", u"Puede ver el formulario de procesos"),
        )
