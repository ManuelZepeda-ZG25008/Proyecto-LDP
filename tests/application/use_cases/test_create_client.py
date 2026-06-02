import pytest
from unittest.mock import Mock
from src.application.use_cases.create_client import CreateClientUseCase, ClientAlreadyExistsError

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def mock_mapper(mocker):
    return mocker.patch('src.application.use_cases.create_client.ClientMapper')

def test_create_client_success(mock_repo, mock_mapper):
    mock_repo.get_by_id.return_value = None 
    use_case = CreateClientUseCase(mock_repo)
    
    dummy_dto = Mock(id="CLI-001")
    mock_mapper.to_entity.return_value = "dummy_entity"
    mock_mapper.to_response_dto.return_value = "dummy_response"

    result = use_case.execute(dummy_dto)

    mock_repo.get_by_id.assert_called_once_with("CLI-001")
    mock_repo.save.assert_called_once_with("dummy_entity")
    assert result == "dummy_response"

def test_create_client_already_exists_raises_error(mock_repo):
    mock_repo.get_by_id.return_value = "existing_client"
    use_case = CreateClientUseCase(mock_repo)
    dummy_dto = Mock(id="CLI-001")

    with pytest.raises(ClientAlreadyExistsError) as exc_info:
        use_case.execute(dummy_dto)
    
    assert "ya está registrado" in str(exc_info.value)
    mock_repo.save.assert_not_called()