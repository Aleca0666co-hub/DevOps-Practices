
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