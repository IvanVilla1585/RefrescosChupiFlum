from __future__ import unicode_literals

from django.db import models

class Proveedore(models.Model):
    nit = models.CharField(max_length=20, unique=True)
    nombre_empresa = models.CharField(max_length=120)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    correo_empresa = models.EmailField(unique=True, blank=True, null=True)
    nombre_contacto = models.CharField(max_length=50, blank=True, null=True)
    apellido_contacto = models.CharField(max_length=50, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True)
    correo_contacto = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        ordering = ('id',)
