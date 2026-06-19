from unittest.mock import Mock
from src.application.mappers.package_mapper import PackageMapper
from src.domain.entities.package import Package

def test_to_entity_maps_correctly():
    dummy_dto = Mock()
    dummy_dto.id = "PKG-001"
    dummy_dto.descripcion = "Laptop Dell"
    dummy_dto.peso = 2.5
    dummy_dto.destinatario_id = "CLI-001"
    dummy_dto.direccion_entrega = "Colonia Escalon Calle 5 Casa 10"

    entity = PackageMapper.to_entity(dummy_dto)

    assert isinstance(entity, Package)
    assert entity.id == "PKG-001"
    assert entity.descripcion == "Laptop Dell"
    assert entity.peso == 2.5

def test_to_response_dto_maps_correctly(mocker):
    mock_response_class = mocker.patch('src.application.mappers.package_mapper.PackageResponseDTO')

    entity = Package(
        id="PKG-002",
        descripcion="Tablet Samsung",
        peso=1.2,
        destinatario_id="CLI-002",
        direccion_entrega="Colonia Miramonte Calle 8 Casa 14",
        estado="En tránsito"
    )

    PackageMapper.to_response_dto(entity)

    mock_response_class.assert_called_once_with(
        id="PKG-002",
        descripcion="Tablet Samsung",
        peso=1.2,
        destinatario_id="CLI-002",
        direccion_entrega="Colonia Miramonte Calle 8 Casa 14",
        estado="En tránsito"
    )
