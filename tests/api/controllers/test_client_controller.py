import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.controllers.client_controller import router  
from src.api.middleware.error_handler import register_error_handlers

from src.application.dtos.client_dto import ClientResponseDTO
from src.domain.exceptions import ResourceNotFoundError, ResourceAlreadyExistsError, DomainValidationError

# CONFIGURACIÓN DEL ENTORNO DE PRUEBAS DE API
app = FastAPI()
app.include_router(router)
register_error_handlers(app) # conexion de los manejadores de error personalizados

client = TestClient(app)

# Un DTO de respuesta falso para reciclar en los tests
dummy_response = ClientResponseDTO(
    id="CLI-001",
    nombre="Juan",
    apellido="Perez",
    email="juan@mail.com",
    telefono="7777-8888",
    direccion="Santa Ana"
)

# TESTS ENDPOINTS CLIENTES
@patch("src.api.controllers.client_controller.CreateClientUseCase.execute")
def test_create_client_endpoint_201(mock_execute):
    # Simulamos que el caso de uso responde exitosamente
    mock_execute.return_value = dummy_response
    
    payload = {
        "id": "CLI-001",
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "juan@mail.com",
        "telefono": "7777-8888",
        "direccion": "Santa Ana"
    }
    
    response = client.post("/clients/", json=payload)
    
    assert response.status_code == 201
    assert response.json()["nombre"] == "Juan"

@patch("src.api.controllers.client_controller.CreateClientUseCase.execute")
def test_create_client_endpoint_409_conflict(mock_execute):
    # Simulamos que el caso de uso detecta un duplicado y lanza tu error personalizado
    mock_execute.side_effect = ResourceAlreadyExistsError("El cliente ya está registrado.")
    
    response = client.post("/clients/", json={
        "id": "CLI-001", "nombre": "Juan", "apellido": "P", "email": "a@b.com", "telefono": "12345678", "direccion": "Calle"
    })
    
    assert response.status_code == 409
    assert response.json()["error"] == "Conflicto de Datos"

@patch("src.api.controllers.client_controller.GetAllClientsUseCase.execute")
def test_get_all_clients_endpoint_200(mock_execute):
    mock_execute.return_value = [dummy_response]
    
    response = client.get("/clients/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1

@patch("src.api.controllers.client_controller.GetClientByIdUseCase.execute")
def test_get_client_by_id_endpoint_200(mock_execute):
    mock_execute.return_value = dummy_response
    
    response = client.get("/clients/CLI-001")
    
    assert response.status_code == 200
    assert response.json()["id"] == "CLI-001"

@patch("src.api.controllers.client_controller.GetClientByIdUseCase.execute")
def test_get_client_by_id_endpoint_404_not_found(mock_execute):
    mock_execute.side_effect = ResourceNotFoundError("El cliente no existe.")
    
    response = client.get("/clients/CLI-999")
    
    assert response.status_code == 404
    assert response.json()["error"] == "Recurso No Encontrado"

@patch("src.api.controllers.client_controller.UpdateClientUseCase.execute")
def test_update_client_endpoint_400_validation_error(mock_execute):
    mock_execute.side_effect = DomainValidationError("El email no tiene un formato válido.")
    
    response = client.put("/clients/CLI-001", json={
        "nombre": "Juan", "apellido": "P", "email": "correo_malo", "telefono": "12345678", "direccion": "Calle"
    })
    
    assert response.status_code == 400
    assert response.json()["error"] == "Validación de Negocio"

@patch("src.api.controllers.client_controller.DeleteClientUseCase.execute")
def test_delete_client_endpoint_204(mock_execute):
    # No devuelve nada, solo ejecuta
    mock_execute.return_value = None
    
    response = client.delete("/clients/CLI-001")
    
    assert response.status_code == 204