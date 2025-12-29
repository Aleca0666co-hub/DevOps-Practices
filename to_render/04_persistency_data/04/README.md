
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
