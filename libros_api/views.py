from rest_framework import viewsets, filters  # Importar filters
# Importar backend de filtros
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count  # Para annotate
from .models import Autor, Libro
from .serializers import AutorSerializer, LibroSerializer


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    # Habilitar búsqueda y ordenación
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'apellido']  # Campos por los que buscar
    # Campos por los que ordenar
    ordering_fields = ['nombre', 'apellido', 'fecha_nacimiento']


class LibroViewSet(viewsets.ModelViewSet):
    # queryset = Libro.objects.all() # Queryset básico
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]  # Añadir DjangoFilterBackend
    # Campos para filtros exactos o relacionados
    filterset_fields = ['fecha_publicacion', 'autores', 'autores__nombre']
    search_fields = ['titulo', 'isbn', 'autores__nombre',
                     'autores__apellido']  # Campos para búsqueda textual
    ordering_fields = ['titulo', 'fecha_publicacion']  # Campos para ordenar

    # c. Consulta compleja (Requisito 3b): Anotar número de autores y permitir filtrar por título y nombre de autor
    def get_queryset(self):
        """
        Sobrescribimos get_queryset para añadir lógica personalizada.
        Anotamos cada libro con la cantidad de autores.
        """
        queryset = Libro.objects.annotate(
            # Añade un campo 'numero_autores' a cada libro
            numero_autores=Count('autores')
        ).order_by('titulo')  # Ordenamos por defecto por título

        # Ejemplo de filtro complejo adicional (opcional, los filtros básicos ya están con filter_backends)
        # titulo_contiene = self.request.query_params.get('titulo_contiene', None)
        # if titulo_contiene:
        #     queryset = queryset.filter(titulo__icontains=titulo_contiene)

        return queryset

    # Sobreescribir el serializer para incluir el campo anotado (opcional pero recomendado)
    def get_serializer_class(self):
        # Si quisiéramos un serializer distinto para la lista que incluya numero_autores
        # if self.action == 'list':
        #     # Aquí podrías definir un LibroListSerializer que incluya 'numero_autores'
        #     # return LibroListSerializer
        #     pass
        return LibroSerializer  # Usamos el mismo por simplicidad
