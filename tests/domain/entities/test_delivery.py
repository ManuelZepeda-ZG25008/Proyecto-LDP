import pytest
from src.domain.entities.delivery import Delivery, InvalidDeliveryError


def test_create_valid_delivery():
    delivery = Delivery(
        id="DEL-001",
        package_id="PKG-001",
        client_id="CLI-001",
        direccion_destino="Colonia Escalon Calle 5 Casa 10",
        estado="pendiente",
        fecha_entrega_estimada="2025-07-10",
        notas="Llamar antes de entregar"
    )
    assert delivery.id == "DEL-001"
    assert delivery.estado == "pendiente"
    assert delivery.package_id == "PKG-001"


def test_delivery_empty_id_raises_error():
    with pytest.raises(InvalidDeliveryError) as exc_info:
        Delivery(
            id="   ",  # ID vacío
            package_id="PKG-001",
            client_id="CLI-001",
            direccion_destino="Colonia Escalon Calle 5 Casa 10",
            estado="pendiente",
            fecha_entrega_estimada="2025-07-10",
            notas=""
        )
    assert "id" in str(exc_info.value).lower()


def test_delivery_empty_package_id_raises_error():
    with pytest.raises(InvalidDeliveryError) as exc_info:
        Delivery(
            id="DEL-001",
            package_id="   ",  # package_id vacío
            client_id="CLI-001",
            direccion_destino="Colonia Escalon Calle 5 Casa 10",
            estado="pendiente",
            fecha_entrega_estimada="2025-07-10",
            notas=""
        )
    assert "paquete" in str(exc_info.value).lower()


def test_delivery_empty_client_id_raises_error():
    with pytest.raises(InvalidDeliveryError) as exc_info:
        Delivery(
            id="DEL-001",
            package_id="PKG-001",
            client_id="   ",  # client_id vacío
            direccion_destino="Colonia Escalon Calle 5 Casa 10",
            estado="pendiente",
            fecha_entrega_estimada="2025-07-10",
            notas=""
        )
    assert "cliente" in str(exc_info.value).lower()


def test_delivery_short_address_raises_error():
    with pytest.raises(InvalidDeliveryError) as exc_info:
        Delivery(
            id="DEL-001",
            package_id="PKG-001",
            client_id="CLI-001",
            direccion_destino="Cal",  # Muy corta
            estado="pendiente",
            fecha_entrega_estimada="2025-07-10",
            notas=""
        )
    assert "demasiado corta" in str(exc_info.value).lower()


def test_delivery_invalid_estado_raises_error():
    with pytest.raises(InvalidDeliveryError) as exc_info:
        Delivery(
            id="DEL-001",
            package_id="PKG-001",
            client_id="CLI-001",
            direccion_destino="Colonia Escalon Calle 5 Casa 10",
            estado="despachado",  # Estado fuera del conjunto permitido
            fecha_entrega_estimada="2025-07-10",
            notas=""
        )
    assert "no es válido" in str(exc_info.value)


def test_delivery_all_valid_estados():
    """Verifica que los cuatro estados permitidos son aceptados sin error."""
    for estado in ["pendiente", "en_transito", "entregado", "cancelado"]:
        delivery = Delivery(
            id="DEL-001",
            package_id="PKG-001",
            client_id="CLI-001",
            direccion_destino="Colonia Escalon Calle 5 Casa 10",
            estado=estado,
            fecha_entrega_estimada="2025-07-10",
            notas=""
        )
        assert delivery.estado == estado


def test_delivery_empty_fecha_raises_error():
    with pytest.raises(InvalidDeliveryError) as exc_info:
        Delivery(
            id="DEL-001",
            package_id="PKG-001",
            client_id="CLI-001",
            direccion_destino="Colonia Escalon Calle 5 Casa 10",
            estado="pendiente",
            fecha_entrega_estimada="   ",  # Fecha vacía
            notas=""
        )
    assert "fecha" in str(exc_info.value).lower()
