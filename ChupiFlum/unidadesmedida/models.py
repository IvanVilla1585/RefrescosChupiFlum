from __future__ import unicode_literals

from django.db import models

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=100)
    equivalencia = models.DecimalField(decimal_places=2, max_digits=16)
    code = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('id',)
        db_table = 'unidades_de_medidas'
        permissions = (
            ("form_view_unidadmedida", u"Formulario unidades de medidas"),
        )
