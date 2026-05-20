from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.domain.exceptions import DomainValidationError, ResourceNotFoundError, ResourceAlreadyExistsError

def register_error_handlers(app: FastAPI) -> None:
    """Registra manejadores para las excepciones base del sistema."""

    @app.exception_handler(DomainValidationError)
    async def domain_validation_handler(request: Request, exc: DomainValidationError):
        return JSONResponse(
            status_code=400,
            content={"error": "Validación de Negocio", "message": str(exc)}
        )

    @app.exception_handler(ResourceNotFoundError)
    async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": "Recurso No Encontrado", "message": str(exc)}
        )

    @app.exception_handler(ResourceAlreadyExistsError)
    async def resource_already_exists_handler(request: Request, exc: ResourceAlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"error": "Conflicto de Datos", "message": str(exc)}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "message": "Algo tronó feo en el servidor, maje."}
        )