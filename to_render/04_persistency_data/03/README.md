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