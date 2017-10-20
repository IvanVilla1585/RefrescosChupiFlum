from django.contrib import admin
from .models import ProductoTerminado

@admin.register(ProductoTerminado)
class ProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'categoria_id', 'costo_produccion', 'precio_venta',)
    list_filter = ('nombre',)
    search_fields = (
        'nombre',
        'categoria__nombre',
        )
