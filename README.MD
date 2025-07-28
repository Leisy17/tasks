# Tasks

## Descripción del proyecto

Este proyecto es una aplicación web construida con FastAPI y PostgreSQL. Utiliza Docker para contenerización, Alembic para migraciones de base de datos y Uvicorn como servidor ASGI.

---

## Configuración del entorno local

1. Crea y activa un entorno virtual:

   ```
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```
2. Instal las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Crea un .env en la raíz del proyecto con las siguientes variables:
   ```
   POSTGRES_USER=usuario
   POSTGRES_PASSWORD=contraseña
   POSTGRES_DB=nombre_db
   DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
   ```
4. Aplica las migraciones. Usa Crtl+Shift+P -> Tasks: Run Task -> bash y luego en tu ambiente virtual ejecuta:
   ```
   alembic upgrade head
   ```
5. Ejecuta la aplicación localmente con F5 o:
   ```
   PYTHONPATH=src uvicorn main:app --reload
   ```

## Ejecutar la aplicación en Docker

1. Construir y levantar los contenedores:
    ```docker-compose up --build```

2. La aplicación estará disponible en: http://localhost:8001

3. Para aplicar migraciones manualmente dentro del contenedor:

    ```
    docker exec -it crehana_app sh
    PYTHONPATH=src alembic upgrade head
    exit
    ```

## Ejecutar pruebas

1. Ejecuta las pruebas con pytest:

    ```
    pytest
    ```





