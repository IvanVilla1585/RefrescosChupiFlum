from django.contrib import admin
from .models import UnidadMedida

@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'equivalencia', 'descripcion',)
    list_filter = ('nombre',)
