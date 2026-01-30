from fastapi import FastAPI
import psycopg2
import os
from pydantic import BaseModel

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

# Modelo para recibir datos en JSON
class Producto(BaseModel):
    id: int
    nombre: str
    precio: float

@app.get("/productos")
def obtener_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, precio FROM productos;")
    rows = cur.fetchall()
    conn.close()
    return {"productos": rows}

@app.post("/productos")
def agregar_producto(producto: Producto):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO productos (id, nombre, precio) VALUES (%s, %s, %s);",
        (producto.id, producto.nombre, producto.precio)
    )
    conn.commit()
    conn.close()
    return {"mensaje": "Producto agregado correctamente", "producto": producto.dict()}
