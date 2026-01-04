---

## 3️⃣ Ejercicio práctico FINAL

### Red entre contenedores + FastAPI + consumo de datos

### 🧠 Escenario

* **Contenedor A:** Proporciona datos (API simple)
* **Contenedor B:** Consume esos datos
* **Contenedor B:** Expone una API FastAPI con documentación (`/docs`)

---

## 📦 Paso 1: Crear la red

```bash
docker network create red_api
```

---

## 📦 Paso 2: Contenedor A (Proveedor de datos)

### `data_api.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/data")
def get_data():
    return {"mensaje": "Hola desde el contenedor proveedor"}
```

### `Dockerfile`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY data_api.py .
CMD ["uvicorn", "data_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Construir y ejecutar:

```bash
docker build -t data_api .
docker run -d --name proveedor --network red_api data_api
```

---

## 📦 Paso 3: Contenedor B (Consumidor + FastAPI)

### `consumer_api.py`

```python
import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/consume")
def consume():
    response = requests.get("http://proveedor:8000/data")
    return {
        "origen": "contenedor consumidor",
        "datos_recibidos": response.json()
    }
```

### `Dockerfile`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn requests
COPY consumer_api.py .
CMD ["uvicorn", "consumer_api:app", "--host", "0.0.0.0", "--port", "8001"]
```

Construir y ejecutar:

```bash
docker build -t consumer_api .
docker run -d --name consumidor \
  --network red_api \
  -p 8001:8001 \
  consumer_api
```

---

## 🌐 Paso 4: Probar la comunicación

Abre en tu navegador:

```
http://localhost:8001/docs
```

Prueba el endpoint:

```
GET /consume
```

✔ El contenedor **consumidor** accede al contenedor **proveedor** usando el **nombre del contenedor como hostname**.

---

## 🧠 Conceptos clave aprendidos

* Docker usa DNS interno
* No se necesitan IPs manuales
* FastAPI se integra perfectamente con Docker
* `/docs` viene incluido automáticamente

---

Si quieres, en el siguiente paso puedo:

* Pasar esto a **docker-compose**
* Agregar **volúmenes**
* Explicar **host vs bridge**
* Hacer un ejercicio tipo **examen práctico**

Solo dime 👍
