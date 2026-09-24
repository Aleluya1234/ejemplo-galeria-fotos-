"""
Actividad · paso 1 (slide 20): "Modelo + Admin: registra tu modelo en Django Admin".

Con esto la Foto ya se puede crear/editar/borrar desde /admin/ sin escribir
ninguna vista. Es el CRUD "gratis" de Django.
"""
from django.contrib import admin

from .models import Foto


@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "publicada", "creada")
    list_filter = ("publicada", "autor")
    search_fields = ("titulo", "descripcion")
