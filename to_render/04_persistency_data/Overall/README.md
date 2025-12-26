

# 🧱 1. ¿Qué significa **bind** y **mounts** en Docker?

### 🔹 **Mount**
“Mount” es el concepto general: **montar algo del host dentro del contenedor**.  
Docker tiene 3 tipos de mounts:

| Tipo | Qué es | Cuándo usar |
|------|--------|-------------|
| **bind mount** | Montas una carpeta/archivo del host tal cual | Desarrollo local, hot‑reload, ver archivos en tiempo real |
| **volume** | Un volumen gestionado por Docker | Persistencia real en producción |
| **tmpfs** | Montado en RAM | Datos temporales |

### 🔹 **Bind mount**
Un **bind** es un tipo de mount donde **Docker usa exactamente la carpeta del host**.

Ejemplo:

```bash
docker run -v $(pwd)/data:/app/data myimage
```

Aquí `/data` en tu máquina se refleja dentro del contenedor en `/app/data`.

---

# 🗃️ 2. Cinco ejercicios básicos de persistencia de datos con Docker  
De nivel 1 a nivel 5, usando SQLite y PostgreSQL.

---

## 🟢 **Ejercicio 1 — Persistencia simple con bind mount (archivo de texto)**  
**Objetivo:** entender qué es un bind mount.

1. Crea una carpeta `data/`
2. Ejecuta:

```bash
docker run --rm -it \
  -v $(pwd)/data:/data \
  alpine sh
```

3. Dentro del contenedor:

```sh
echo "hola docker" > /data/archivo.txt
```

4. Sal del contenedor y revisa `data/archivo.txt` en tu host.

---

## 🟡 **Ejercicio 2 — Persistencia con SQLite + bind mount**  
**Objetivo:** ver cómo un archivo `.db` persiste fuera del contenedor.

1. Crea carpeta `sqlite/`
2. Ejecuta:

```bash
docker run --rm -it \
  -v $(pwd)/sqlite:/db \
  alpine sh
```

3. Instala sqlite dentro del contenedor:

```sh
apk add sqlite
sqlite3 /db/test.db "CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);"
sqlite3 /db/test.db "INSERT INTO users(name) VALUES ('Alejandro');"
```

4. Sal y revisa que `sqlite/test.db` existe en tu host.

---

## 🟠 **Ejercicio 3 — Persistencia con Volumes (Docker-managed)**  
**Objetivo:** usar volúmenes reales de Docker.

1. Crea un volumen:

```bash
docker volume create mydata
```

2. Ejecuta:

```bash
docker run -it --rm \
  -v mydata:/data \
  alpine sh
```

3. Crea un archivo dentro del contenedor:

```sh
echo "persisto" > /data/test.txt
```

4. Sal y vuelve a entrar con otro contenedor usando el mismo volumen.  
Verás el archivo.

---

## 🔵 **Ejercicio 4 — PostgreSQL con volumen (nivel básico)**  
**Objetivo:** levantar PostgreSQL con persistencia real.

```bash
docker run -d \
  --name pg \
  -e POSTGRES_PASSWORD=1234 \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

- El volumen `pgdata` guarda la base de datos.
- Puedes borrar el contenedor y los datos siguen.

Prueba conectarte:

```bash
docker exec -it pg psql -U postgres
```

---

## 🔴 **Ejercicio 5 — FastAPI + SQLAlchemy + PostgreSQL con persistencia**  
**Objetivo:** un mini‑stack real.

Estructura:

```
project/
 ├─ app/
 │   ├─ main.py
 │   └─ models.py
 ├─ docker-compose.yml
```

### `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: 1234
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    depends_on:
      - db
    volumes:
      - .:/app
    ports:
      - "8000:8000"

volumes:
  pgdata:
```

Levanta todo:

```bash
docker compose up
```

Ahora tienes FastAPI conectado a PostgreSQL con persistencia real.

---

# 🧩 3. ¿Puedes decir que “manejas PostgreSQL” si usas SQLAlchemy?

Sí, **totalmente**.  
Y te explico por qué, desde la perspectiva profesional:

### ✔️ SQLAlchemy **no reemplaza** tu conocimiento de la base de datos  
SQLAlchemy es un ORM, pero:

- Tú defines modelos que se traducen a SQL real.
- Tú configuras conexiones, pools, transacciones.
- Tú entiendes índices, relaciones, constraints.
- Tú depuras errores de PostgreSQL.
- Tú escribes queries complejas cuando hace falta.

### ✔️ En tu CV puedes poner perfectamente:

**“PostgreSQL (a través de SQLAlchemy)”**  
o  
**“Experiencia trabajando con PostgreSQL en entornos FastAPI + SQLAlchemy”**

Esto es estándar en la industria.

### ✔️ Incluso empresas esperan que uses un ORM  
No esperan que escribas SQL puro todo el día.

---

# 🎁 ¿Quieres que te prepare un mini‑proyecto educativo completo?
Con:

- FastAPI  
- SQLAlchemy  
- SQLite para desarrollo  
- PostgreSQL para producción  
- Docker + docker-compose  
- Documentación bilingüe estilo Alejandro  

Si quieres, lo armamos paso a paso.