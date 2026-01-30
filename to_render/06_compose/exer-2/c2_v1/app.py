from fastapi import FastAPI
import psycopg2
import os

app = FastAPI(title="API Contenedor C2_V1")

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

@app.get("/productos")
def obtener_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, precio FROM productos;")
    rows = cur.fetchall()
    conn.close()
    return {"productos": rows}