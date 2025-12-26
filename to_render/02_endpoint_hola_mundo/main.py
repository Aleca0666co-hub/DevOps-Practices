from fastapi import FastAPI

app = FastAPI(title="Prove with docker and fastapi")

@app.get("/")
def read_root():
    return {"mensaje": "Hola desde FastAPI en Docker"}

@app.get("/saludo")
def saludo():
    return {"saludo": "Docker + FastAPI funcionando 🚀"}
