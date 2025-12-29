
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