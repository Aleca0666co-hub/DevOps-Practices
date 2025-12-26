
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