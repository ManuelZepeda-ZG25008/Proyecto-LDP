from fastapi import FastAPI
from src.infrastructure.persistence.sqlite_connection import init_db
from src.api.middleware.error_handler import register_error_handlers
from src.api.controllers.client_controller import router as client_router
from src.api.controllers.delivery_controller import router as delivery_router  # ← esta línea

app = FastAPI(
    title="Sistema de Control de Paquetería ",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    init_db()

register_error_handlers(app)

app.include_router(client_router)
app.include_router(delivery_router)  # ← y esta

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Bienvenido al Sistema de Control de Paquetería"}