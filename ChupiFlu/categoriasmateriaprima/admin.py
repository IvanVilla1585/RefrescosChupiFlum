from django.contrib import admin
from .models import CategoriaMateriaPrima

@admin.register(CategoriaMateriaPrima)
class CategoriaMateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', )
    list_filter = ('nombre',)
