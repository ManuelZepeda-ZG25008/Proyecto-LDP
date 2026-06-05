import pytest
from unittest.mock import Mock
from src.application.use_cases.create_delivery import CreateDeliveryUseCase, DeliveryAlreadyExistsError
from src.application.use_cases.get_delivery import (
    GetDeliveryByIdUseCase,
    GetAllDeliveriesUseCase,
    UpdateDeliveryUseCase,
    DeleteDeliveryUseCase,
    DeliveryNotFoundError
)


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def mock_create_mapper(mocker):
    return mocker.patch('src.application.use_cases.create_delivery.DeliveryMapper')

@pytest.fixture
def mock_get_mapper(mocker):
    return mocker.patch('src.application.use_cases.get_delivery.DeliveryMapper')


# ── CreateDeliveryUseCase ────────────────────────────────────────────────────

def test_create_delivery_success(mock_repo, mock_create_mapper):
    mock_repo.get_by_id.return_value = None  # No existe aún
    use_case = CreateDeliveryUseCase(mock_repo)

    dummy_dto = Mock(id="DEL-001")
    mock_create_mapper.to_entity.return_value = "dummy_entity"
    mock_create_mapper.to_response_dto.return_value = "dummy_response"

    result = use_case.execute(dummy_dto)

    mock_repo.get_by_id.assert_called_once_with("DEL-001")
    mock_repo.save.assert_called_once_with("dummy_entity")
    assert result == "dummy_response"

def test_create_delivery_already_exists_raises_error(mock_repo):
    mock_repo.get_by_id.return_value = "existing_delivery"  # Ya existe
    use_case = CreateDeliveryUseCase(mock_repo)
    dummy_dto = Mock(id="DEL-001")

    with pytest.raises(DeliveryAlreadyExistsError) as exc_info:
        use_case.execute(dummy_dto)

    assert "ya está registrada" in str(exc_info.value)
    mock_repo.save.assert_not_called()


# ── GetDeliveryByIdUseCase ───────────────────────────────────────────────────

def test_get_delivery_by_id_success(mock_repo, mock_get_mapper):
    mock_repo.get_by_id.return_value = "delivery_entity"
    use_case = GetDeliveryByIdUseCase(mock_repo)
    mock_get_mapper.to_response_dto.return_value = "delivery_response"

    result = use_case.execute("DEL-001")

    mock_repo.get_by_id.assert_called_once_with("DEL-001")
    assert result == "delivery_response"

def test_get_delivery_by_id_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None
    use_case = GetDeliveryByIdUseCase(mock_repo)

    with pytest.raises(DeliveryNotFoundError) as exc_info:
        use_case.execute("DEL-999")

    assert "no existe" in str(exc_info.value)


# ── GetAllDeliveriesUseCase ──────────────────────────────────────────────────

def test_get_all_deliveries_success(mock_repo, mock_get_mapper):
    mock_repo.get_all.return_value = ["delivery1", "delivery2"]
    use_case = GetAllDeliveriesUseCase(mock_repo)
    mock_get_mapper.to_response_dto.side_effect = ["response1", "response2"]

    result = use_case.execute()

    mock_repo.get_all.assert_called_once()
    assert result == ["response1", "response2"]


# ── UpdateDeliveryUseCase ────────────────────────────────────────────────────

def test_update_delivery_success(mock_repo, mock_get_mapper):
    mock_entity = Mock()
    mock_repo.get_by_id.return_value = mock_entity
    use_case = UpdateDeliveryUseCase(mock_repo)

    dummy_update_dto = Mock(
        direccion_destino="Colonia Nueva Calle 1 Casa 2",
        estado="en_transito",
        fecha_entrega_estimada="2025-08-15",
        notas="En camino"
    )
    mock_get_mapper.to_response_dto.return_value = "updated_response"

    result = use_case.execute("DEL-001", dummy_update_dto)

    mock_entity.update_info.assert_called_once_with(
        direccion_destino="Colonia Nueva Calle 1 Casa 2",
        estado="en_transito",
        fecha_entrega_estimada="2025-08-15",
        notas="En camino"
    )
    mock_repo.save.assert_called_once_with(mock_entity)
    assert result == "updated_response"

def test_update_delivery_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None
    use_case = UpdateDeliveryUseCase(mock_repo)
    dummy_update_dto = Mock()

    with pytest.raises(DeliveryNotFoundError):
        use_case.execute("DEL-999", dummy_update_dto)

    mock_repo.save.assert_not_called()


# ── DeleteDeliveryUseCase ────────────────────────────────────────────────────

def test_delete_delivery_success(mock_repo):
    mock_repo.get_by_id.return_value = "existing_delivery"
    use_case = DeleteDeliveryUseCase(mock_repo)

    use_case.execute("DEL-001")

    mock_repo.delete.assert_called_once_with("DEL-001")

def test_delete_delivery_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None
    use_case = DeleteDeliveryUseCase(mock_repo)

    with pytest.raises(DeliveryNotFoundError):
        use_case.execute("DEL-999")

    mock_repo.delete.assert_not_called()
