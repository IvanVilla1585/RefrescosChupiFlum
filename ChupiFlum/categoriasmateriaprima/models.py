from __future__ import unicode_literals

from django.db import models

class CategoriaMateriaPrima(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('id',)
        db_table='categorias_materias_primas'
