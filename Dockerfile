# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /src

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos del proyecto a la imagen
COPY ./src /src
COPY requirements.txt /src


# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto en el que FastAPI correrá
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI usando Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

