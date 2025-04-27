import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Autor, Libro
from .serializers import LibroSerializer  # Importar serializer para comparar

# Datos iniciales para las pruebas


def crear_autor(nombre, apellido):
    return Autor.objects.create(nombre=nombre, apellido=apellido)


def crear_libro(titulo, isbn, autores_lista):
    libro = Libro.objects.create(titulo=titulo, isbn=isbn)
    libro.autores.set(autores_lista)
    return libro


class LibroAPITests(TestCase):
    def setUp(self):
        # Configuración inicial para cada test
        self.autor1 = crear_autor('Test', 'Autor Uno')
        self.autor2 = crear_autor('Test', 'Autor Dos')
        self.libro1 = crear_libro(
            'Libro de Prueba 1', '1111111111', [self.autor1])
        self.libro2 = crear_libro('Libro de Prueba 2', '2222222222', [
                                  self.autor1, self.autor2])

        # URLs comunes
        # 'libro' es el basename que definimos en urls.py
        self.libros_list_url = reverse('libro-list')
        self.libro1_detail_url = reverse(
            'libro-detail', kwargs={'pk': self.libro1.pk})

    def test_listar_libros(self):
        """Verifica que se puedan listar los libros."""
        response = self.client.get(self.libros_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)

    def test_obtener_detalle_libro(self):
        """Verifica que se pueda obtener el detalle de un libro específico."""
        response = self.client.get(self.libro1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], self.libro1.titulo)
        # Verifica autores anidados
        self.assertEqual(len(response.data['autores_detalle']), 1)
        self.assertEqual(
            response.data['autores_detalle'][0]['nombre'], self.autor1.nombre)

    def test_crear_libro(self):
        """Verifica que se pueda crear un libro."""
        nuevo_libro_data = {
            'titulo': 'Nuevo Libro Test',
            'isbn': '3333333333',
            # Enviar lista de IDs de autores
            'autores': [self.autor1.pk, self.autor2.pk]
        }
        response = self.client.post(
            self.libros_list_url, nuevo_libro_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Libro.objects.count(), 8)
        nuevo_libro = Libro.objects.get(isbn='3333333333')
        self.assertEqual(nuevo_libro.titulo, 'Nuevo Libro Test')
        self.assertEqual(nuevo_libro.autores.count(), 2)

    def test_actualizar_libro(self):
        """Verifica que se pueda actualizar un libro completamente (PUT)."""
        libro_actualizado_data = {
            'titulo': 'Libro Actualizado',
            'isbn': self.libro1.isbn,  # Reutiliza el ISBN existente
            'autores': [self.autor2.pk]  # Cambiamos el autor
        }
        response = self.client.put(  # <--- CAMBIO AQUÍ
            self.libro1_detail_url,
            data=json.dumps(libro_actualizado_data),  # <--- CAMBIO AQUÍ
            content_type='application/json'  # <--- CAMBIO AQUÍ
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.libro1.refresh_from_db()
        self.assertEqual(self.libro1.titulo, 'Libro Actualizado')
        self.assertEqual(self.libro1.autores.count(), 1)
        self.assertEqual(self.libro1.autores.first().pk, self.autor2.pk)

    def test_actualizar_parcialmente_libro(self):
        """Verifica que se pueda actualizar parcialmente un libro (PATCH)."""
        libro_patch_data = {
            'titulo': 'Libro Parcialmente Actualizado'
        }
        response = self.client.patch(  # <--- CAMBIO AQUÍ
            self.libro1_detail_url,
            data=json.dumps(libro_patch_data),  # <--- CAMBIO AQUÍ
            content_type='application/json'  # <--- CAMBIO AQUÍ
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.libro1.refresh_from_db()
        self.assertEqual(self.libro1.titulo, 'Libro Parcialmente Actualizado')
        # Verifica que el ISBN no cambió
        self.assertEqual(self.libro1.isbn, '1111111111')

    def test_eliminar_libro(self):
        """Verifica que se pueda eliminar un libro."""
        response = self.client.delete(self.libro1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Libro.objects.count(), 6)
        with self.assertRaises(Libro.DoesNotExist):
            Libro.objects.get(pk=self.libro1.pk)
