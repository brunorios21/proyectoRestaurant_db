# Imagen base oficial de Python
#(slim: una versión más pequeña y más segura, pero con menos funcionalidad)
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que corre Flask
EXPOSE 8080

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]
