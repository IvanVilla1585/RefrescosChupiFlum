from django.contrib import admin
from .models import MateriaPrima

@admin.register(MateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'unidad_medida', 'categoria', 'cantidad', )
    list_filter = ('nombre',)
    search_fields = (
        'nombre',
        'categoria__nombre',
        'unidad_medida__nombre',
        )
