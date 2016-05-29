from __future__ import unicode_literals

from django.db import models

class Perfil(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.nombre
