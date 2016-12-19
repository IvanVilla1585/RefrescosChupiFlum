from django.contrib import admin
from .models import Presentacion

@admin.register(Presentacion)
class AdminCategoria(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'estado',)
    list_filter = ('nombre',)
