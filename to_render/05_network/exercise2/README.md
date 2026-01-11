Perfecto, Alejandro.  
Vamos a hacer **una recapitulación completa**, bien pedagógica y clara, con **3 contenedores**:

- **c1_v1** → FastAPI que consume la DB  
- **c2_v1** → FastAPI que consume la DB  
- **db_v1** → PostgreSQL con datos iniciales  
- **red:** `mi_red`

Todo usando **Docker CLI**, sin Compose, para que entiendas perfectamente el patrón antes de pasar al siguiente nivel.

---

# 🟦 1. Crear la red bridge personalizada

```bash
docker network create mi_red
```

---

# 🟦 2. Contenedor de PostgreSQL (db_v1)

## 📌 Dockerfile (db_v1 no necesita Dockerfile, usamos imagen oficial)

Creamos el contenedor:

```bash
docker run -d \
  --name db_v1 \
  --network mi_red \
  -e POSTGRES_USER=ale \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=demo \
  postgres:15
```

## 📌 Insertar datos iniciales

Esperamos unos segundos y luego entramos:

```bash
docker exec -it db_v1 psql -U ale -d demo
```

Dentro de PostgreSQL:

```sql
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    precio INT
);

INSERT INTO productos (nombre, precio) VALUES
('Laptop', 1200),
('Mouse', 25),
('Teclado', 45);
```

Listo: ya tenemos datos para consumir.

---

# 🟦 3. Backend FastAPI para c1_v1 y c2_v1

Ambos contenedores tendrán **el mismo código**, solo cambia el nombre del contenedor.

## 📁 Estructura

```
c1_v1/
  Dockerfile
  app.py

c2_v1/
  Dockerfile
  app.py
```

---

# 🟦 4. Código FastAPI (app.py)

Este backend consulta PostgreSQL y expone una API con título personalizado.

```python
from fastapi import FastAPI
import psycopg2
import os

app = FastAPI(title="API Contenedor C1_V1")

DB_HOST = os.getenv("DB_HOST", "db_v1")
DB_USER = os.getenv("DB_USER", "ale")
DB_PASS = os.getenv("DB_PASS", "1234")
DB_NAME = os.getenv("DB_NAME", "demo")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )

@app.get("/productos")
def obtener_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, precio FROM productos;")
    rows = cur.fetchall()
    conn.close()
    return {"productos": rows}
```

Para **c2_v1**, cambia solo el título:

```python
app = FastAPI(title="API Contenedor C2_V1")
```

---

# 🟦 5. Dockerfile para c1_v1 y c2_v1

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY app.py .

RUN pip install fastapi uvicorn psycopg2-binary

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# 🟦 6. Construir las imágenes

```bash
docker build -t c1_v1 ./c1_v1
docker build -t c2_v1 ./c2_v1
```

---

# 🟦 7. Levantar los contenedores FastAPI

### Contenedor c1_v1

```bash
docker run -d \
  --name c1_v1 \
  --network mi_red \
  -e DB_HOST=db_v1 \
  -e DB_USER=ale \
  -e DB_PASS=1234 \
  -e DB_NAME=demo \
  -p 8001:8000 \
  c1_v1
```

### Contenedor c2_v1

```bash
docker run -d \
  --name c2_v1 \
  --network mi_red \
  -e DB_HOST=db_v1 \
  -e DB_USER=ale \
  -e DB_PASS=1234 \
  -e DB_NAME=demo \
  -p 8002:8000 \
  c2_v1
```

---

# 🟦 8. Probar desde el host

### API de c1_v1

```
http://localhost:8001/productos
```

### API de c2_v1

```
http://localhost:8002/productos
```

Ambas deben devolver:

```json
{
  "productos": [
    [1, "Laptop", 1200],
    [2, "Mouse", 25],
    [3, "Teclado", 45]
  ]
}
```

---

# 🟦 9. Probar desde dentro de los contenedores (para reforzar networking)

```bash
docker exec -it c1_v1 bash
curl http://db_v1:5432   # conexión a la DB
```

```bash
docker exec -it c2_v1 bash
curl http://c1_v1:8000/productos
```

Todo funciona porque **están en la misma red bridge**.

---

# 🟦 10. Qué aprendiste con este ejercicio

✔ Cómo crear una red bridge personalizada  
✔ Cómo conectar 3 contenedores a la misma red  
✔ Cómo usar PostgreSQL dentro de Docker  
✔ Cómo inicializar datos en la DB  
✔ Cómo consumir la DB desde FastAPI  
✔ Cómo exponer APIs con títulos diferentes  
✔ Cómo comunicar contenedores por nombre (DNS interno)  
✔ Cómo publicar puertos para acceder desde el host  

Este es el **último paso perfecto antes de pasar a Docker Compose**.

---

Si quieres, ahora puedo convertir **exactamente este mismo proyecto** en una versión con **docker-compose.yml**, para que veas cómo se simplifica todo.