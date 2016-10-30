from django.contrib import admin
from .models import Maquina

@admin.register(Maquina)
class UnidadesMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'capacidad', 'unidad_medida','tiempo',)
    list_filter = ('nombre',)
    search_fields = (
        'nombre',
        'unidad_medida__nombre',
        )
