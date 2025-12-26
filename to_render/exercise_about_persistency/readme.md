¡Perfecto! Vamos a armar **3 ejercicios prácticos y sencillos** que puedas hacer en tu Play with Docker. Te dejo el detalle de cada uno, con explicación, código y pasos.

---

# **Ejercicio 1 – Persistencia con volumen (MySQL/Postgres)**

**Objetivo:** Que los datos de la base sobrevivan aunque el contenedor se detenga.

### 1️⃣ Comandos

```bash
# Crear volumen
docker volume create datos_db

# Levantar contenedor Postgres con volumen
docker run -d \
  --name mi_db \
  -v datos_db:/var/lib/postgresql/data \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=testdb \
  -p 5432:5432 \
  postgres:15
```

### 2️⃣ Pasos a probar

1. Conectar desde FastAPI o `psql` y crear una tabla.
2. Detener el contenedor:

```bash
docker stop mi_db
docker rm mi_db
```

3. Levantar de nuevo:

```bash
docker run -d \
  --name mi_db \
  -v datos_db:/var/lib/postgresql/data \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=testdb \
  -p 5432:5432 \
  postgres:15
```

✅ Los datos creados siguen ahí gracias al **volumen**.

---

# **Ejercicio 2 – Persistencia de código con bind mount (FastAPI)**

**Objetivo:** Que puedas editar código sin reconstruir la imagen.

### 1️⃣ Comandos

```bash
# Desde la carpeta del proyecto con main.py y requirements.txt
docker run -d \
  --name mi_fastapi \
  -v $(pwd):/app \
  -p 8000:8000 \
  python:3.11-slim \
  uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2️⃣ Pasos a probar

1. Cambia algo en `main.py` (por ejemplo un mensaje en la ruta `/`).
2. Verifica que los cambios se reflejan **sin reconstruir la imagen**.
3. Detén y borra el contenedor:

```bash
docker stop mi_fastapi
docker rm mi_fastapi
```

✅ El código sigue en tu carpeta del host gracias al **bind mount**.

---

# **Ejercicio 3 – Variables de entorno en FastAPI**

**Objetivo:** Configurar FastAPI usando variables de entorno y exponerlas a Docker.

### 1️⃣ Código `main.py`:

```python
from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_env():
    secret = os.getenv("MI_SECRET", "No definido")
    return {"MI_SECRET": secret}
```

### 2️⃣ Comandos

```bash
docker run -d \
  --name fastapi_env \
  -p 8000:8000 \
  -e MI_SECRET=MiValorSecreto \
  -v $(pwd):/app \
  python:3.11-slim \
  uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3️⃣ Pasos a probar

1. Accede a `http://localhost:8000/`
2. Deberías ver:

```json
{"MI_SECRET": "MiValorSecreto"}
```

3. Cambia el valor de `MI_SECRET` y vuelve a levantar el contenedor para ver cómo se refleja.

---

# ✅ Qué aprendes con estos ejercicios

* **Ej1:** Volúmenes → persistencia de datos de DB
* **Ej2:** Bind mounts → persistencia de código / desarrollo rápido
* **Ej3:** Variables de entorno → parametrización de la app sin tocar código

---

Si quieres, puedo armarte **una versión combinada de estos 3 ejercicios en un solo Docker Compose**, para levantar FastAPI + DB + variables de entorno **en un solo comando**, ideal para Play with Docker y tu flujo de trabajo.

¿Quieres que haga eso?
