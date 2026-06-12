from django.contrib import admin
from .models import Evento, SetMusical


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'data', 'hora', 'local', 'capacidade']
    list_filter = ['data']
    search_fields = ['nome', 'local']
    ordering = ['data', 'hora']


@admin.register(SetMusical)
class SetAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'tipo', 'data']
    list_filter = ['tipo', 'data']
    search_fields = ['nome']
    ordering = ['-data', 'nome']
