import pytest
from src.domain.entities.client import Client, InvalidClientError 

def test_create_valid_client():
    client = Client(
        id="CLI-123",
        nombre="Juan",
        apellido="Perez",
        email="juan.perez@email.com",
        telefono="7777-8888",
        direccion="Santa Ana"
    )
    assert client.id == "CLI-123"
    assert client.nombre == "Juan"
    assert client.telefono == "7777-8888"

def test_client_empty_nombre_raises_error():
    with pytest.raises(InvalidClientError) as exc_info:
        Client(
            id="CLI-123",
            nombre="   ", # Nombre vacío
            apellido="Perez",
            email="juan@email.com",
            telefono="7777-8888",
            direccion="Santa Ana"
        )
    assert "nombre" in str(exc_info.value).lower()

def test_client_invalid_email_raises_error():
    with pytest.raises(InvalidClientError) as exc_info:
        Client(
            id="CLI-123",
            nombre="Juan",
            apellido="Perez",
            email="correo_invalido.com", # Falta el @
            telefono="7777-8888",
            direccion="Santa Ana"
        )
    assert "formato válido" in str(exc_info.value)

def test_client_short_phone_raises_error():
    with pytest.raises(InvalidClientError) as exc_info:
        Client(
            id="CLI-123",
            nombre="Juan",
            apellido="Perez",
            email="juan@email.com",
            telefono="1234", # Muy corto
            direccion="Santa Ana"
        )
    assert "al menos 8 dígitos" in str(exc_info.value).lower()

def test_client_short_address_raises_error():
    with pytest.raises(InvalidClientError) as exc_info:
        Client(
            id="CLI-123",
            nombre="Juan",
            apellido="Perez",
            email="juan@email.com",
            telefono="7777-8888",
            direccion="San" # Muy corta
        )
    assert "demasiado corta" in str(exc_info.value).lower()