from unittest.mock import Mock
from src.application.mappers.delivery_mapper import DeliveryMapper
from src.domain.entities.delivery import Delivery


def test_to_entity_maps_correctly():
    dummy_dto = Mock()
    dummy_dto.id = "DEL-001"
    dummy_dto.package_id = "PKG-001"
    dummy_dto.client_id = "CLI-001"
    dummy_dto.direccion_destino = "Colonia Escalon Calle 5 Casa 10"
    dummy_dto.estado = "pendiente"
    dummy_dto.fecha_entrega_estimada = "2025-07-10"
    dummy_dto.notas = "Llamar antes de entregar"

    entity = DeliveryMapper.to_entity(dummy_dto)

    assert isinstance(entity, Delivery)
    assert entity.id == "DEL-001"
    assert entity.package_id == "PKG-001"
    assert entity.estado == "pendiente"


def test_to_response_dto_maps_correctly(mocker):
    # Mockeamos el DTO de respuesta para verificar cómo se le envían los datos
    mock_response_class = mocker.patch('src.application.mappers.delivery_mapper.DeliveryResponseDTO')

    entity = Delivery(
        id="DEL-002",
        package_id="PKG-002",
        client_id="CLI-002",
        direccion_destino="Colonia Miramonte Calle 8 Casa 14",
        estado="en_transito",
        fecha_entrega_estimada="2025-08-01",
        notas="Entregar en porteria"
    )

    DeliveryMapper.to_response_dto(entity)

    # Verificamos que el DTO se instancie exactamente con la info de la entidad
    mock_response_class.assert_called_once_with(
        id="DEL-002",
        package_id="PKG-002",
        client_id="CLI-002",
        direccion_destino="Colonia Miramonte Calle 8 Casa 14",
        estado="en_transito",
        fecha_entrega_estimada="2025-08-01",
        notas="Entregar en porteria"
    )
