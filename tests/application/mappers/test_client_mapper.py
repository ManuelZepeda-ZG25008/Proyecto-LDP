from unittest.mock import Mock
from src.application.mappers.client_mapper import ClientMapper
from src.domain.entities.client import Client

def test_to_entity_maps_correctly():
    dummy_dto = Mock()
    dummy_dto.id = "CLI-001"
    dummy_dto.nombre = "Carlos"
    dummy_dto.apellido = "Gomez"
    dummy_dto.email = "carlos@mail.com"
    dummy_dto.telefono = "7777-8888"
    dummy_dto.direccion = "San Salvador"
    
    entity = ClientMapper.to_entity(dummy_dto)
    
    assert isinstance(entity, Client)
    assert entity.id == "CLI-001"
    assert entity.nombre == "Carlos"
    assert entity.telefono == "7777-8888"

def test_to_response_dto_maps_correctly(mocker):
    # Mockeamos el DTO de respuesta para verificar cómo se le envían los datos
    mock_response_class = mocker.patch('src.application.mappers.client_mapper.ClientResponseDTO')
    
    entity = Client(
        id="CLI-002",
        nombre="Maria",
        apellido="Lopez",
        email="maria@mail.com",
        telefono="7777-5678",
        direccion="San Miguel"
    )
    
    ClientMapper.to_response_dto(entity)
    
    # Verificamos que el DTO se instancie exactamente con la info de la entidad
    mock_response_class.assert_called_once_with(
        id="CLI-002",
        nombre="Maria",
        apellido="Lopez",
        email="maria@mail.com",
        telefono="7777-5678",
        direccion="San Miguel"
    )