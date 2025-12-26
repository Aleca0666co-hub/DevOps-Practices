Perfecto, Alejandro. Vamos con un **Ejercicio 3** mucho más realista:  
**FastAPI + PostgreSQL + docker-compose + variables de entorno**.  
Este es el tipo de setup que usarías en Render, Railway o cualquier entorno productivo.

Lo voy a hacer **minimalista, didáctico y reproducible**, como te gusta.

---

# 🔵 **Ejercicio 3 — FastAPI + PostgreSQL + Variables de entorno con docker-compose**

## 🎯 Objetivo
- Crear variables de entorno en un archivo `.env`
- Usarlas en `docker-compose.yml`
- Consumirlas desde FastAPI
- Exponerlas en un endpoint para verificar que funcionan

---

# 📁 Estructura del proyecto

```
project/
 ├─ app/
 │   ├─ main.py
 │   └─ config.py
 ├─ Dockerfile
 ├─ docker-compose.yml
 └─ .env
```

---

# 🧩 1. Archivo `.env`

Este archivo **no se copia dentro de la imagen**, solo lo usa docker-compose.

```
POSTGRES_USER=alejandro
POSTGRES_PASSWORD=1234
POSTGRES_DB=mydb
APP_ENV=production
APP_SECRET=supersecreto
```

---

# 🧱 2. `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:16
    env_file:
      - .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    env_file:
      - .env
    environment:
      APP_ENV: ${APP_ENV}
      APP_SECRET: ${APP_SECRET}
      DATABASE_URL: "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"
    depends_on:
      - db
    ports:
      - "8000:8000"

volumes:
  pgdata:
```

---

# 🐍 3. `config.py` — leer variables de entorno

```python
import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")
    app_secret: str = os.getenv("APP_SECRET", "none")
    database_url: str = os.getenv("DATABASE_URL", "none")

settings = Settings()
```

---

# 🚀 4. `main.py` — exponer las variables

```python
from fastapi import FastAPI
from .config import settings

app = FastAPI()

@app.get("/env")
def read_env():
    return {
        "APP_ENV": settings.app_env,
        "APP_SECRET": settings.app_secret,
        "DATABASE_URL": settings.database_url
    }
```

---

# 🐳 5. `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY app ./app

RUN pip install fastapi uvicorn pydantic

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# ▶️ 6. Levantar todo

```bash
docker compose up --build
```

---

# 🔍 7. Probar

Abre:

```
http://localhost:8000/env
```

Deberías ver algo como:

```json
{
  "APP_ENV": "production",
  "APP_SECRET": "supersecreto",
  "DATABASE_URL": "postgresql://alejandro:1234@db:5432/mydb"
}
```

Esto confirma que:

- docker-compose leyó `.env`
- FastAPI recibió las variables
- Las expuso correctamente

---

# 🎁 ¿Quieres que prepare un **Ejercicio 4** donde FastAPI realmente se conecte a PostgreSQL usando SQLAlchemy y lea datos reales desde la DB usando las variables de entorno?