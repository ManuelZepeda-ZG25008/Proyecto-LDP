# src/domain/exceptions.py

class DomainValidationError(Exception):
    """Base para cualquier error de validación de reglas de negocio (HTTP 400)."""
    pass

class ResourceNotFoundError(Exception):
    """Base para cuando algo no se encuentra en la base de datos (HTTP 404)."""
    pass

class ResourceAlreadyExistsError(Exception):
    """Base para conflictos de duplicidad de datos (HTTP 409)."""
    pass