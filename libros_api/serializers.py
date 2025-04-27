from rest_framework import serializers
from .models import Autor, Libro


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        # Incluimos 'libros' para ver los IDs de los libros asociados
        fields = ['id', 'nombre', 'apellido', 'fecha_nacimiento', 'libros']
        # Hacemos 'libros' de solo lectura aquí, se maneja desde el LibroSerializer
        read_only_fields = ['libros']


class LibroSerializer(serializers.ModelSerializer):
    # Para mostrar nombres en lugar de IDs (opcional, mejora la legibilidad)
    autores_detalle = AutorSerializer(
        source='autores', many=True, read_only=True)

    class Meta:
        model = Libro
        # 'autores' se usa para crear/actualizar la relación (espera IDs)
        # 'autores_detalle' se usa para mostrar la información completa (solo lectura)
        fields = ['id', 'titulo', 'fecha_publicacion',
                  'isbn', 'autores', 'autores_detalle']
        extra_kwargs = {
            # 'autores' solo se usa para escribir (recibe lista de IDs)
            'autores': {'write_only': True}
        }

    # Opcional: Validación personalizada (ejemplo)
    def validate_isbn(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError(
                "El ISBN debe contener solo números.")
        if value and len(value) not in [10, 13]:
            raise serializers.ValidationError(
                "El ISBN debe tener 10 o 13 dígitos.")
        return value
