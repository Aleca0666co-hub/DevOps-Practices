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