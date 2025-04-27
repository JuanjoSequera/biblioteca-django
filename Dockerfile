# Dockerfile

# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema (si son necesarias, ej. para PostgreSQL)
# RUN apt-get update && apt-get install -y postgresql-client libpq-dev gcc

# Instalar dependencias de Python
# Copiar solo el archivo de requerimientos primero para aprovechar el caché de Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto al directorio de trabajo
COPY . /app/

# Exponer el puerto en el que correrá la aplicación Django (usualmente 8000)
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación (se sobreescribirá en docker-compose)
# CMD ["gunicorn", "biblioteca_project.wsgi:application", "--bind", "0.0.0.0:8000"]