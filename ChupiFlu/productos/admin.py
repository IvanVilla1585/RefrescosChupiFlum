from django.contrib import admin
from .models import ProductoTerminado
from actions import export_as_excel

@admin.register(ProductoTerminado)
class ProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'categoria', 'costo_produccion', 'precio_venta',)
    list_filter = ('nombre',)
    search_fields = (
        'nombre',
        'categoria__nombre',
        )
    actions = (export_as_excel,)
