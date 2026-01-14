from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/env")
def read_env():
    return {
        "MY_VAR": os.getenv("MY_VAR", "No definida"),
        "OTHER_VAR": os.getenv("OTHER_VAR", "No definida")
    }
