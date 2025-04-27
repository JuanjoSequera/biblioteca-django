#!/bin/bash

# deploy.sh

# Detener y eliminar contenedores, redes y volúmenes anteriores (opcional, pero útil para empezar limpio)
echo "Deteniendo y eliminando contenedores anteriores (si existen)..."
docker-compose down -v --remove-orphans

# Construir las imágenes definidas en docker-compose.yml (o reconstruir si hubo cambios)
echo "Construyendo imágenes Docker..."
docker-compose build

# Levantar los servicios definidos en docker-compose.yml en modo detached (-d)
echo "Levantando los servicios con Docker Compose..."
docker-compose up -d

# Opcional: Mostrar logs de los contenedores (descomentar si quieres ver la salida)
# echo "Mostrando logs..."
# docker-compose logs -f

echo "¡Despliegue completado! La aplicación debería estar accesible en http://localhost:8000"

# Opcional: Ejecutar pruebas dentro del contenedor web después de levantar los servicios
# echo "Ejecutando pruebas dentro del contenedor..."
# docker-compose exec web python manage.py test libros_api

exit 0