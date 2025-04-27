# Desafío Técnico - API Biblioteca (Django)

Hola, este es mi proyecto. Es una API sencilla hecha con Django y Django REST Framework para manejar libros y autores. Usa Docker.

## Requisitos para Probar

Necesitas tener instalados:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (Normalmente viene con Docker Desktop)

## Ejecutar y Probar el Proyecto

Estos son los pasos básicos para levantar la aplicación:

1.  **Clona este repositorio:**

    ```bash
    git clone [https://github.com/JuanjoSequera/biblioteca-django.git](https://github.com/JuanjoSequera/biblioteca-django.git)
    cd biblioteca-django
    ```

2.  **Levanta los contenedores con Docker:**
    En tu terminal ejecuta:

    ```bash
    bash deploy.sh
    ```

3.  **Accede a la aplicación:**

    - **API:** Puedes probarla en estas URLs:
      - Libros: `http://localhost:8000/api/libros/`
      - Autores: `http://localhost:8000/api/autores/`
    - **Panel de Administración Django:** `http://localhost:8000/admin/`

4.  **Entrar al Admin:**
    Para explorar el panel de admin, primero crea un usuario administrador. Abre **otra terminal** en la misma carpeta y corre:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    Sigue las instrucciones para crear tu usuario y contraseña.

## Correr las Pruebas

Para ejecutar las pruebas que escribe:

```bash
docker-compose exec web python manage.py test libros_api
```
