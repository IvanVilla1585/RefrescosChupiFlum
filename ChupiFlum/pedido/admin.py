from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'proveedor', 'usuario', 'fecha', 'total',)
    list_filter = ('descripcion', 'proveedor', 'usuario')
    search_fields = (
        'descripcion',
        'proveedor',
        'usuario',
        )
