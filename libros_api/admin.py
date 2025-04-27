from django.contrib import admin
from .models import Autor, Libro


class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'isbn', 'fecha_publicacion', 'mostrar_autores')
    list_filter = ('fecha_publicacion', 'autores')
    search_fields = ('titulo', 'isbn', 'autores__nombre', 'autores__apellido')
    filter_horizontal = ('autores',)  # Mejora la interfaz para ManyToMany

    def mostrar_autores(self, obj):
        return ", ".join([autor.nombre + " " + autor.apellido for autor in obj.autores.all()])
    mostrar_autores.short_description = 'Autores'


class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido')


admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro, LibroAdmin)
