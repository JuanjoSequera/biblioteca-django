from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AutorViewSet, LibroViewSet

# Crea un router
router = DefaultRouter()
# Registra los viewsets con el router
router.register(r'autores', AutorViewSet, basename='autor')
router.register(r'libros', LibroViewSet, basename='libro')

# Las URLs de la API son generadas automáticamente por el router
urlpatterns = [
    path('', include(router.urls)),
]
