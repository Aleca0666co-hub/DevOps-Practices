Perfecto, Alejandro.  
Ahora vamos a **convertir EXACTAMENTE el mismo proyecto** (c1_v1, c2_v1 y db_v1) en **Docker Compose**, para que veas cómo todo se simplifica brutalmente.

Este es el paso final antes de que empieces a trabajar como un pro con Compose.

---

# 🟦 1. Estructura del proyecto

```
project/
  docker-compose.yml
  c1_v1/
    Dockerfile
    app.py
  c2_v1/
    Dockerfile
    app.py
```

Los Dockerfiles y los `app.py` son **los mismos** que ya hicimos.

---

# 🟦 2. docker-compose.yml (versión completa y profesional)

Aquí está el archivo **listo para usar**:

```yaml
version: "3.9"

services:
  db_v1:
    image: postgres:15
    container_name: db_v1
    environment:
      POSTGRES_USER: ale
      POSTGRES_PASSWORD: 1234
      POSTGRES_DB: demo
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - mi_red

  c1_v1:
    build: ./c1_v1
    container_name: c1_v1
    environment:
      DB_HOST: db_v1
      DB_USER: ale
      DB_PASS: 1234
      DB_NAME: demo
    ports:
      - "8001:8000"
    depends_on:
      - db_v1
    networks:
      - mi_red

  c2_v1:
    build: ./c2_v1
    container_name: c2_v1
    environment:
      DB_HOST: db_v1
      DB_USER: ale
      DB_PASS: 1234
      DB_NAME: demo
    ports:
      - "8002:8000"
    depends_on:
      - db_v1
    networks:
      - mi_red

networks:
  mi_red:

volumes:
  pgdata:
```

---

# 🟦 3. ¿Qué simplifica Compose?

### ✔ Ya no creas la red manualmente  
Compose crea `mi_red` automáticamente.

### ✔ Ya no necesitas `docker run`  
Todo se levanta con:

```bash
docker compose up --build
```

### ✔ Los contenedores se resuelven por nombre  
`c1_v1` y `c2_v1` pueden llamar a:

```
http://db_v1:5432
```

### ✔ Los puertos quedan claros  
- c1_v1 → `localhost:8001`
- c2_v1 → `localhost:8002`

### ✔ La base de datos ahora es persistente  
Gracias al volumen:

```yaml
volumes:
  - pgdata:/var/lib/postgresql/data
```

---

# 🟦 4. Probar las APIs

### Contenedor c1_v1

```
http://localhost:8001/productos
```

### Contenedor c2_v1

```
http://localhost:8002/productos
```

Ambos deben devolver:

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

# 🟦 5. Verificar networking interno

Puedes entrar a c1_v1:

```bash
docker exec -it c1_v1 bash
```

Y probar:

```bash
curl http://db_v1:5432
```

O desde c2_v1:

```bash
curl http://c1_v1:8000/productos
```

Todo funciona porque Compose crea una **red interna con DNS automático**.

---

# 🟦 6. Qué acabas de lograr

✔ Convertiste un proyecto manual en uno profesional  
✔ Aprendiste cómo Compose maneja redes, DNS y dependencias  
✔ Entendiste cómo se conectan múltiples servicios  
✔ Ya puedes documentar esto en tus repos educativos  
✔ Estás listo para pasar a proyectos más grandes (frontend, workers, redis, etc.)

---

Si quieres, puedo hacer:

- un **diagrama visual** de la arquitectura  
- una **versión con variables .env**  
- una **versión con healthchecks**  
- una **versión con pgAdmin** para ver la DB gráficamente  

Tú eliges hacia dónde seguimos.