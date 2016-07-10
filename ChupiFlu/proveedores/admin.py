from django.contrib import admin
from .models import Proveedore
from actions import export_as_excel

@admin.register(Proveedore)
class ProveedoreAdmin(admin.ModelAdmin):
    list_display = ('nit', 'nombre_empresa', 'direccion', 'telefono', 'fax', 'correo_empresa',
                    'nombre_contacto', 'apellido_contacto', 'telefono_contacto', 'correo_contacto',)
    list_filter = ('nit', 'nombre_empresa',)
    search_fields = (
        'nombre_empresa',
        'nit',
        )
    actions = (export_as_excel,)
