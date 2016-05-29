from django.contrib import admin
from .models import Categoria

@admin.register(Categoria)
class AdminCategoria(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion',)
    list_filter = ('nombre',)
