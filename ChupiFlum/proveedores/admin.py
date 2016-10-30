from django.contrib import admin
from .models import Proveedore

@admin.register(Proveedore)
class ProveedoreAdmin(admin.ModelAdmin):
    list_display = ('nit', 'empresa', 'direccion', 'telefono', 'fax', 'correo_empresa',
                    'nombre_contacto', 'apellido_contacto', 'telefono_contacto', 'correo_contacto',)
    list_filter = ('nit', 'empresa',)
    search_fields = (
        'empresa',
        'nit',
        )
