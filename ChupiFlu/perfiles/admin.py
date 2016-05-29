from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class AdminPerfil(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion',)
    list_filter = ('nombre',)
