from django.contrib import admin
from .models import EstadosOrdenes

@admin.register(EstadosOrdenes)
class EstadosOrdenesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion',)
    list_filter = ('nombre',)
    search_fields = (
        'nombre',
        )
