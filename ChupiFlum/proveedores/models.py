from __future__ import unicode_literals

from django.db import models

class Proveedore(models.Model):
    nit = models.CharField(max_length=20, unique=True)
    empresa = models.CharField(max_length=120)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fax = models.CharField(max_length=15, blank=True, null=True)
    correo_empresa = models.EmailField(unique=True, blank=True, null=True)
    nombre_contacto = models.CharField(max_length=50)
    apellido_contacto = models.CharField(max_length=50, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=15)
    correo_contacto = models.EmailField(unique=True, blank=True, null=True)
    estado = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.empresa

    class Meta:
        ordering = ('id',)
        db_table = 'proveedores'
        permissions = (
            ("form_view_proveedor", "Puede ver el formulario de proveedores"),
        )
