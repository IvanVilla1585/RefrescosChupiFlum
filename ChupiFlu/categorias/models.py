from __future__ import unicode_literals

from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.nombre
