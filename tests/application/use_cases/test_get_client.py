import pytest
from unittest.mock import Mock
from src.application.use_cases.get_client import (
    GetClientByIdUseCase, 
    GetAllClientsUseCase, 
    UpdateClientUseCase, 
    DeleteClientUseCase, 
    ClientNotFoundError
)

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def mock_mapper(mocker):
    return mocker.patch('src.application.use_cases.get_client.ClientMapper')

def test_get_client_by_id_success(mock_repo, mock_mapper):
    mock_repo.get_by_id.return_value = "client_entity"
    use_case = GetClientByIdUseCase(mock_repo)
    mock_mapper.to_response_dto.return_value = "client_response"

    result = use_case.execute("CLI-001")

    mock_repo.get_by_id.assert_called_once_with("CLI-001")
    assert result == "client_response"

def test_get_client_by_id_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None 
    use_case = GetClientByIdUseCase(mock_repo)

    with pytest.raises(ClientNotFoundError) as exc_info:
        use_case.execute("CLI-999")
    
    assert "no existe" in str(exc_info.value)

def test_get_all_clients_success(mock_repo, mock_mapper):
    mock_repo.get_all.return_value = ["client1", "client2"]
    use_case = GetAllClientsUseCase(mock_repo)
    mock_mapper.to_response_dto.side_effect = ["response1", "response2"]

    result = use_case.execute()

    mock_repo.get_all.assert_called_once()
    assert result == ["response1", "response2"]

def test_update_client_success(mock_repo, mock_mapper):
    mock_entity = Mock()
    mock_repo.get_by_id.return_value = mock_entity 
    use_case = UpdateClientUseCase(mock_repo)
    
    dummy_update_dto = Mock(
        nombre="Nuevo Nombre", 
        apellido="Nuevo Apellido", 
        email="nuevo@mail.com", 
        telefono="1234", 
        direccion="Calle Falsa 123"
    )
    mock_mapper.to_response_dto.return_value = "updated_response"

    result = use_case.execute("CLI-001", dummy_update_dto)

    mock_entity.update_info.assert_called_once_with(
        nombre="Nuevo Nombre",
        apellido="Nuevo Apellido",
        email="nuevo@mail.com",
        telefono="1234",
        direccion="Calle Falsa 123"
    )
    mock_repo.save.assert_called_once_with(mock_entity)
    assert result == "updated_response"

def test_update_client_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None
    use_case = UpdateClientUseCase(mock_repo)
    dummy_update_dto = Mock()

    with pytest.raises(ClientNotFoundError):
        use_case.execute("CLI-999", dummy_update_dto)
    
    mock_repo.save.assert_not_called()

def test_delete_client_success(mock_repo):
    mock_repo.get_by_id.return_value = "existing_client"
    use_case = DeleteClientUseCase(mock_repo)

    use_case.execute("CLI-001")

    mock_repo.delete.assert_called_once_with("CLI-001")

def test_delete_client_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None
    use_case = DeleteClientUseCase(mock_repo)

    with pytest.raises(ClientNotFoundError):
        use_case.execute("CLI-999")
    
    mock_repo.delete.assert_not_called()