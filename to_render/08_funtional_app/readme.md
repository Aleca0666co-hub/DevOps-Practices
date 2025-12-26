Buenísima la idea, Alejandro. Vamos a armar **un ejemplo mínimo pero realista** que puedas usar como referencia y como material educativo.

Todo con:

- **FastAPI** (backend)
- **SQLite + SQLAlchemy** (persistencia)
- **Frontend vanilla JS** (mínimo pero funcional)
- **Docker + docker-compose + volumen para la DB**
- **Deploy en Render usando GitHub** (sin Docker Hub)

---

## 1. Visión general del proyecto

Vamos a construir:

- **Una API FastAPI** que maneja una lista de “items” simples (ej: notas, tareas, lo que quieras).
- **Base de datos SQLite** persistida en un archivo `data/app.db`.
- **Frontend con HTML + JS** que:
  - Llama a la API (GET/POST).
  - Muestra la lista de items.
- **Un solo contenedor** que:
  - Sirve la API.
  - Sirve el frontend estático desde FastAPI.
- **docker-compose** para:
  - Crear un volumen para la DB.
  - Levantar el servicio para desarrollo/producción con un solo comando.

---

## 2. Estructura del proyecto

Te propongo esta estructura:

```bash
fastapi-docker-example/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   └── static/
│       ├── index.html
│       └── app.js
├── data/               # (carpeta de la DB, se persistirá con volumen)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 3. Paso 1: Backend FastAPI + SQLite + SQLAlchemy

### 3.1 `requirements.txt`

```txt
fastapi
uvicorn[standard]
sqlalchemy
pydantic
```

### 3.2 `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Ruta relativa a la carpeta /app dentro del contenedor
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DB_DIR, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(DB_DIR, 'app.db')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

### 3.3 `app/models.py`

```python
from sqlalchemy import Column, Integer, String
from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
```

### 3.4 `app/schemas.py`

```python
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

    class Config:
        orm_mode = True
```

### 3.5 `app/main.py`

```python
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, SessionLocal
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Static frontend
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API
@app.get("/api/items", response_model=list[schemas.ItemRead])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@app.post("/api/items", response_model=schemas.ItemRead)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

---

## 4. Paso 2: Frontend vanilla JS mínimo

### 4.1 `app/static/index.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>FastAPI + Docker + SQLite</title>
</head>
<body>
  <h1>Items</h1>

  <form id="item-form">
    <input type="text" id="title" placeholder="Título" required />
    <input type="text" id="description" placeholder="Descripción" required />
    <button type="submit">Crear</button>
  </form>

  <ul id="items-list"></ul>

  <script src="/static/app.js"></script>
</body>
</html>
```

### 4.2 `app/static/app.js`

```javascript
const API_URL = "/api/items";

const form = document.getElementById("item-form");
const titleInput = document.getElementById("title");
const descriptionInput = document.getElementById("description");
const itemsList = document.getElementById("items-list");

async function fetchItems() {
  const res = await fetch(API_URL);
  const data = await res.json();
  itemsList.innerHTML = "";
  data.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.id} - ${item.title}: ${item.description}`;
    itemsList.appendChild(li);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const item = {
    title: titleInput.value,
    description: descriptionInput.value,
  };

  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(item),
  });

  titleInput.value = "";
  descriptionInput.value = "";
  await fetchItems();
});

// Inicial
fetchItems();
```

---

## 5. Paso 3: Dockerfile para backend + frontend

### `Dockerfile`

```Dockerfile
FROM python:3.11-slim

# Evitar buffer en logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema si las necesitas (ej: gcc, libpq, etc.)
# RUN apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código
COPY app ./app
COPY data ./data

# Exponemos el puerto interno
EXPOSE 8000

# Comando por defecto: uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 6. Paso 4: docker-compose con volumen para la base de datos

Aquí hacemos que la carpeta `./data` del host se monte dentro del contenedor como `/app/data`, para que el archivo `app.db` persista fuera del contenedor.

### `docker-compose.yml`

```yaml
version: "3.9"

services:
  web:
    build: .
    container_name: fastapi_example
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

### ¿Qué hace cada cosa?

- **`build: .`**: construye la imagen usando el `Dockerfile` en la raíz.
- **`ports: "8000:8000"`**:
  - Puerto 8000 en el host → 8000 en el contenedor.
  - Accedes a `http://localhost:8000`.
- **`volumes: ./data:/app/data`**:
  - Carpeta local `data/` → carpeta `/app/data` en el contenedor.
  - El archivo SQLite vive ahí _(persistente)_.
- **`restart: unless-stopped`**:
  - En producción, el contenedor se reinicia si falla.

### Probar localmente

```bash
docker-compose up --build
```

Luego ve a:

- `http://localhost:8000` → frontend
- `http://localhost:8000/api/items` → API

---

## 7. Paso 5: Subir a GitHub (en lugar de Docker Hub)

1. **Inicializar repo**:
   ```bash
   git init
   git add .
   git commit -m "FastAPI + Docker + SQLite example"
   ```
2. **Crear repo en GitHub** (manual en la web).
3. Conectar:
   ```bash
   git remote add origin git@github.com:tu_usuario/fastapi-docker-example.git
   git push -u origin main
   ```

Render va a leer tu repo y construir la imagen desde el `Dockerfile`.

---

## 8. Paso 6: Deploy en Render usando Dockerfile

En Render:

1. **Crear un nuevo servicio web**.
2. Elegir **"Deploy from GitHub"** y conectar tu repo.
3. Tipo de servicio: **Docker** (Render detecta el `Dockerfile`).
4. Configuración típica:
   - **Branch**: `main`
   - **Root Directory**: `.` (raíz del repo)
   - **Port**: `8000` (el que usamos en `EXPOSE` y en uvicorn)
5. Render construirá la imagen, correrá el contenedor y expondrá una URL pública.

Tu frontend estático seguirá funcionando porque se sirve desde FastAPI.

---

## 9. Instrucciones para “modo producción”

Algunas cosas que cambiaría para producción:

- **Desactivar debug**: ahora no usamos `DEBUG`, pero si lo agregás:
  - Usar `ENV` o variables de entorno en Render, nunca hardcode.
- **Workers de uvicorn/gunicorn**:
  - Para algo más serio, usarías gunicorn + uvicorn workers:
    ```Dockerfile
    CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:8000", "-w", "4"]
    ```
- **Migraciones**:
  - Si el proyecto crece, pasar de `create_all` a Alembic.
- **Seguridad básica**:
  - Usar HTTPS (Render ya lo da).
  - Configurar CORS si el frontend estuviera en otro dominio.
- **Logs**:
  - Mantener `PYTHONUNBUFFERED=1` para logs en tiempo real.
- **Tamaño de imagen**:
  - Puedes luego optimizar con `python:3.11-alpine` o multi-stage builds.

---

Si querés, en el siguiente paso puedo:

- Ajustar esto a un caso más “real” tipo **CRUD de usuarios/tareas**, o  
- Ayudarte a escribir un **README.md bilingüe (ES/EN) bonito**, con todos estos pasos listados para que otros puedan seguirlo.