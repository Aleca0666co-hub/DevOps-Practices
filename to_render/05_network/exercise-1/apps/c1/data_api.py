from fastapi import FastAPI

app = FastAPI()

@app.get("/data")
def get_data():
    return {"mensaje": "Hola desde el contenedor proveedor"}