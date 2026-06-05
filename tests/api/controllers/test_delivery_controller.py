import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.controllers.delivery_controller import router
from src.api.middleware.error_handler import register_error_handlers

from src.application.dtos.delivery_dto import DeliveryResponseDTO
from src.domain.exceptions import ResourceNotFoundError, ResourceAlreadyExistsError, DomainValidationError

# CONFIGURACIÓN DEL ENTORNO DE PRUEBAS DE API
app = FastAPI()
app.include_router(router)
register_error_handlers(app)  # Conexión de los manejadores de error personalizados

client = TestClient(app)

# Un DTO de respuesta falso para reciclar en los tests
dummy_response = DeliveryResponseDTO(
    id="DEL-001",
    package_id="PKG-001",
    client_id="CLI-001",
    direccion_destino="Colonia Escalon Calle 5 Casa 10",
    estado="pendiente",
    fecha_entrega_estimada="2025-07-10",
    notas="Llamar antes de entregar"
)

# TESTS ENDPOINTS ENTREGAS

@patch("src.api.controllers.delivery_controller.CreateDeliveryUseCase.execute")
def test_create_delivery_endpoint_201(mock_execute):
    # Simulamos que el caso de uso responde exitosamente
    mock_execute.return_value = dummy_response

    payload = {
        "id": "DEL-001",
        "package_id": "PKG-001",
        "client_id": "CLI-001",
        "direccion_destino": "Colonia Escalon Calle 5 Casa 10",
        "estado": "pendiente",
        "fecha_entrega_estimada": "2025-07-10",
        "notas": "Llamar antes de entregar"
    }

    response = client.post("/deliveries/", json=payload)

    assert response.status_code == 201
    assert response.json()["estado"] == "pendiente"

@patch("src.api.controllers.delivery_controller.CreateDeliveryUseCase.execute")
def test_create_delivery_endpoint_409_conflict(mock_execute):
    # Simulamos que el caso de uso detecta un duplicado
    mock_execute.side_effect = ResourceAlreadyExistsError("La entrega ya está registrada.")

    response = client.post("/deliveries/", json={
        "id": "DEL-001",
        "package_id": "PKG-001",
        "client_id": "CLI-001",
        "direccion_destino": "Colonia Escalon Calle 5 Casa 10",
        "estado": "pendiente",
        "fecha_entrega_estimada": "2025-07-10",
        "notas": ""
    })

    assert response.status_code == 409
    assert response.json()["error"] == "Conflicto de Datos"

@patch("src.api.controllers.delivery_controller.CreateDeliveryUseCase.execute")
def test_create_delivery_endpoint_400_invalid_estado(mock_execute):
    # Simulamos que la entidad de dominio rechaza el estado inválido
    mock_execute.side_effect = DomainValidationError("El estado 'despachado' no es válido.")

    response = client.post("/deliveries/", json={
        "id": "DEL-002",
        "package_id": "PKG-001",
        "client_id": "CLI-001",
        "direccion_destino": "Colonia Escalon Calle 5 Casa 10",
        "estado": "despachado",
        "fecha_entrega_estimada": "2025-07-10",
        "notas": ""
    })

    assert response.status_code == 400
    assert response.json()["error"] == "Validación de Negocio"

@patch("src.api.controllers.delivery_controller.GetAllDeliveriesUseCase.execute")
def test_get_all_deliveries_endpoint_200(mock_execute):
    mock_execute.return_value = [dummy_response]

    response = client.get("/deliveries/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1

@patch("src.api.controllers.delivery_controller.GetDeliveryByIdUseCase.execute")
def test_get_delivery_by_id_endpoint_200(mock_execute):
    mock_execute.return_value = dummy_response

    response = client.get("/deliveries/DEL-001")

    assert response.status_code == 200
    assert response.json()["id"] == "DEL-001"

@patch("src.api.controllers.delivery_controller.GetDeliveryByIdUseCase.execute")
def test_get_delivery_by_id_endpoint_404_not_found(mock_execute):
    mock_execute.side_effect = ResourceNotFoundError("La entrega no existe.")

    response = client.get("/deliveries/DEL-999")

    assert response.status_code == 404
    assert response.json()["error"] == "Recurso No Encontrado"

@patch("src.api.controllers.delivery_controller.UpdateDeliveryUseCase.execute")
def test_update_delivery_endpoint_200(mock_execute):
    updated = DeliveryResponseDTO(
        id="DEL-001",
        package_id="PKG-001",
        client_id="CLI-001",
        direccion_destino="Colonia Escalon Calle 5 Casa 10",
        estado="en_transito",
        fecha_entrega_estimada="2025-07-10",
        notas="En camino"
    )
    mock_execute.return_value = updated

    response = client.put("/deliveries/DEL-001", json={
        "direccion_destino": "Colonia Escalon Calle 5 Casa 10",
        "estado": "en_transito",
        "fecha_entrega_estimada": "2025-07-10",
        "notas": "En camino"
    })

    assert response.status_code == 200
    assert response.json()["estado"] == "en_transito"

@patch("src.api.controllers.delivery_controller.UpdateDeliveryUseCase.execute")
def test_update_delivery_endpoint_404_not_found(mock_execute):
    mock_execute.side_effect = ResourceNotFoundError("La entrega no existe.")

    response = client.put("/deliveries/DEL-999", json={
        "direccion_destino": "Colonia Escalon Calle 5 Casa 10",
        "estado": "en_transito",
        "fecha_entrega_estimada": "2025-07-10",
        "notas": ""
    })

    assert response.status_code == 404
    assert response.json()["error"] == "Recurso No Encontrado"

@patch("src.api.controllers.delivery_controller.DeleteDeliveryUseCase.execute")
def test_delete_delivery_endpoint_204(mock_execute):
    # No devuelve nada, solo ejecuta
    mock_execute.return_value = None

    response = client.delete("/deliveries/DEL-001")

    assert response.status_code == 204
