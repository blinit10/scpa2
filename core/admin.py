from django.contrib import admin
from .models import *

class FichaAdmin(admin.ModelAdmin):
    list_display = ('mostrar_foto', 'nombre', 'identidad', 'raza')
    list_filter = ('color', 'raza', 'sexo', 'esterilizado')
    list_per_page = 10
    list_display_links = ('mostrar_foto', 'nombre', 'identidad', 'raza')
    search_fields = ['nombre', 'identidad', 'color', 'raza', 'peso']
    fieldsets = (
        ('', {
            # 'classes': ('collapse',),
            'fields': (('nombre', 'identidad'),'raza')
        }),
        ('Otros datos', {
            'fields': ('color','foto', 'mostrar_foto', 'sexo', 'esterilizado', 'peso')}),
        ('QR', {
            'fields': ('mostrar_qr',)}),
    )
    readonly_fields = ('mostrar_foto', 'mostrar_qr')

class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono')
    list_filter = ('veterinario',)
    list_per_page = 10
    list_display_links = ('nombre', 'apellido', 'telefono')
    search_fields = ['nombre', 'apellido', 'telefono', 'edad']
    fieldsets = (
        ('', {
            # 'classes': ('collapse',),
            'fields': (('nombre', 'apellido'),'telefono')
        }),
        ('Otros datos', {
            'fields': ('edad','veterinario')}),
    )

class VisitaAdmin(admin.ModelAdmin):
    list_display = ('visitante', 'fecha')
    list_filter = ('visitante', 'fecha')
    list_per_page = 10
    list_display_links = ('visitante', 'fecha')
    search_fields = ['visitante']
    fieldsets = (
        ('', {
            # 'classes': ('collapse',),
            'fields': ('visitante', 'fecha')
        }),
    )

class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'fecha')
    list_filter = ('fecha','tipo')
    list_per_page = 10
    list_display_links = ('nombre', 'tipo', 'fecha')
    search_fields = ['nombre', 'tipo', 'fecha', 'detalles']
    fieldsets = (
        ('', {
            # 'classes': ('collapse',),
            'fields': (('nombre', 'tipo'),'fecha')
        }),
        ('Otros datos', {
            'fields': ('foto','mostrar_foto','detalles')}),
    )
    readonly_fields = ('mostrar_foto',)

class InformacionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_per_page = 10
    list_display_links = ('__str__',)
    search_fields = ['texto',]
    fieldsets = (
        ('', {
            # 'classes': ('collapse',),
            'fields': (('texto',),)
        }),
    )

class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('ficha', 'fecha')
    list_filter = ('fecha','ficha')
    list_per_page = 10
    list_display_links = ('ficha', 'fecha')
    fieldsets = (
        ('', {
            # 'classes': ('collapse',),
            'fields': (('ficha',),'fecha')
        }),
    )

# Register your models here.
admin.site.register(Ficha, FichaAdmin)
admin.site.register(Visita, VisitaAdmin)
admin.site.register(Visitante,VisitanteAdmin)
admin.site.register(Evento,EventoAdmin)
admin.site.register(Informacion, InformacionAdmin)
admin.site.register(Denuncia, DenunciaAdmin)