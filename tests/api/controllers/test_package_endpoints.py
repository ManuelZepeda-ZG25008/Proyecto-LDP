import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.controllers.package_controller import router
from src.api.middleware.error_handler import register_error_handlers

from src.application.dtos.package_dto import PackageResponseDTO
from src.domain.exceptions import ResourceNotFoundError, ResourceAlreadyExistsError, DomainValidationError

# Configuración del entorno de pruebas
app = FastAPI()
app.include_router(router)
register_error_handlers(app)

client = TestClient(app)

dummy_response = PackageResponseDTO(
    id="PKG-001",
    descripcion="Laptop Dell",
    peso=2.5,
    destinatario_id="CLI-001",
    direccion_entrega="Colonia Escalon Calle 5 Casa 10",
    estado="Pendiente"
)


@patch("src.api.controllers.package_controller.CreatePackageUseCase.execute")
def test_create_package_201(mock_execute):
    mock_execute.return_value = dummy_response

    payload = {
        "id": "PKG-001",
        "descripcion": "Laptop Dell",
        "peso": 2.5,
        "destinatario_id": "CLI-001",
        "direccion_entrega": "Colonia Escalon Calle 5 Casa 10"
    }

    response = client.post("/packages/", json=payload)

    assert response.status_code == 201
    assert response.json()["estado"] == "Pendiente"

@patch("src.api.controllers.package_controller.CreatePackageUseCase.execute")
def test_create_package_409_conflict(mock_execute):
    mock_execute.side_effect = ResourceAlreadyExistsError("El paquete ya existe.")

    response = client.post("/packages/", json={
        "id": "PKG-001",
        "descripcion": "Laptop Dell",
        "peso": 2.5,
        "destinatario_id": "CLI-001",
        "direccion_entrega": "Colonia Escalon Calle 5 Casa 10"
    })

    assert response.status_code == 409
    assert response.json()["error"] == "Conflicto de Datos"

@patch("src.api.controllers.package_controller.CreatePackageUseCase.execute")
def test_create_package_400_invalid(mock_execute):
    mock_execute.side_effect = DomainValidationError("El peso debe ser mayor a cero.")

    response = client.post("/packages/", json={
        "id": "PKG-002",
        "descripcion": "Laptop Dell",
        "peso": -1,
        "destinatario_id": "CLI-001",
        "direccion_entrega": "Colonia Escalon Calle 5 Casa 10"
    })

    assert response.status_code == 400
    assert response.json()["error"] == "Validación de Negocio"

@patch("src.api.controllers.package_controller.GetAllPackagesUseCase.execute")
def test_get_all_packages_200(mock_execute):
    mock_execute.return_value = [dummy_response]

    response = client.get("/packages/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1

@patch("src.api.controllers.package_controller.GetPackageByIdUseCase.execute")
def test_get_package_by_id_200(mock_execute):
    mock_execute.return_value = dummy_response

    response = client.get("/packages/PKG-001")

    assert response.status_code == 200
    assert response.json()["id"] == "PKG-001"

@patch("src.api.controllers.package_controller.GetPackageByIdUseCase.execute")
def test_get_package_by_id_404(mock_execute):
    mock_execute.side_effect = ResourceNotFoundError("Paquete no encontrado.")

    response = client.get("/packages/PKG-999")

    assert response.status_code == 404
    assert response.json()["error"] == "Recurso No Encontrado"

@patch("src.api.controllers.package_controller.UpdatePackageUseCase.execute")
def test_update_package_200(mock_execute):
    updated = PackageResponseDTO(
        id="PKG-001",
        descripcion="Laptop Dell",
        peso=2.5,
        destinatario_id="CLI-001",
        direccion_entrega="Colonia Escalon Calle 5 Casa 10",
        estado="En tránsito"
    )
    mock_execute.return_value = updated

    response = client.put("/packages/PKG-001", json={
        "descripcion": "Laptop Dell",
        "peso": 2.5,
        "direccion_entrega": "Colonia Escalon Calle 5 Casa 10",
        "estado": "En tránsito"
    })

    assert response.status_code == 200
    assert response.json()["estado"] == "En tránsito"

@patch("src.api.controllers.package_controller.UpdatePackageUseCase.execute")
def test_update_package_404(mock_execute):
    mock_execute.side_effect = ResourceNotFoundError("Paquete no encontrado.")

    response = client.put("/packages/PKG-999", json={
        "descripcion": "Laptop Dell",
        "peso": 2.5,
        "direccion_entrega": "Colonia Escalon Calle 5 Casa 10",
        "estado": "En tránsito"
    })

    assert response.status_code == 404
    assert response.json()["error"] == "Recurso No Encontrado"

@patch("src.api.controllers.package_controller.DeletePackageUseCase.execute")
def test_delete_package_204(mock_execute):
    mock_execute.return_value = None

    response = client.delete("/packages/PKG-001")

    assert response.status_code == 204
