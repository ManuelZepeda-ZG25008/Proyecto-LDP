from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Control de Paquetería - DDD",
    description="API robusta bajo principios de Clean Architecture y DDD",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "architecture": "Clean Architecture / DDD",
        "environment": "Development"
    }