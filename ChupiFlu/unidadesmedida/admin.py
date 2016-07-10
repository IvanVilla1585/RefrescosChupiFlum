from django.contrib import admin
from .models import UnidadesMateriaPrima

@admin.register(UnidadesMateriaPrima)
class UnidadesMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'equivalencia', 'descripcion',)
    list_filter = ('nombre',)
