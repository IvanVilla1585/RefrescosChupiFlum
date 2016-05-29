from __future__ import unicode_literals

from django.db import models
from categorias.models import Categoria

class ProductoTerminado(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    categoria = models.ForeignKey(Categoria)
    costo_produccion = models.FloatField()
    precio_venta = models.FloatField()
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre
