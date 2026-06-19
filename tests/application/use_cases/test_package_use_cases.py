import pytest
from unittest.mock import Mock
from src.application.use_cases.create_package import CreatePackageUseCase, PackageAlreadyExistsError
from src.application.use_cases.get_package import (
    GetPackageByIdUseCase,
    GetAllPackagesUseCase,
    UpdatePackageUseCase,
    DeletePackageUseCase,
    PackageNotFoundError
)


@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def mock_mapper(mocker):
    return mocker.patch('src.application.use_cases.create_package.PackageMapper')

@pytest.fixture
def mock_get_mapper(mocker):
    return mocker.patch('src.application.use_cases.get_package.PackageMapper')


def test_create_package_success(mock_repo, mock_mapper):
    mock_repo.get_by_id.return_value = None
    use_case = CreatePackageUseCase(mock_repo)

    dummy_dto = Mock(id="PKG-001")
    mock_mapper.to_entity.return_value = "dummy_entity"
    mock_mapper.to_response_dto.return_value = "dummy_response"

    result = use_case.execute(dummy_dto)

    mock_repo.get_by_id.assert_called_once_with("PKG-001")
    mock_repo.save.assert_called_once_with("dummy_entity")
    assert result == "dummy_response"

def test_create_package_already_exists(mock_repo):
    mock_repo.get_by_id.return_value = "existing_package"
    use_case = CreatePackageUseCase(mock_repo)
    dummy_dto = Mock(id="PKG-001")

    with pytest.raises(PackageAlreadyExistsError):
        use_case.execute(dummy_dto)

    mock_repo.save.assert_not_called()




def test_get_package_by_id_success(mock_repo, mock_get_mapper):
    mock_repo.get_by_id.return_value = "package_entity"
    use_case = GetPackageByIdUseCase(mock_repo)
    mock_get_mapper.to_response_dto.return_value = "package_response"

    result = use_case.execute("PKG-001")

    mock_repo.get_by_id.assert_called_once_with("PKG-001")
    assert result == "package_response"

def test_get_package_by_id_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None
    use_case = GetPackageByIdUseCase(mock_repo)

    with pytest.raises(PackageNotFoundError):
        use_case.execute("PKG-999")

    mock_repo.get_by_id.assert_called_once_with("PKG-999")



def test_get_all_packages_success(mock_repo, mock_get_mapper):
    mock_repo.get_all.return_value = ["pkg1", "pkg2"]
    use_case = GetAllPackagesUseCase(mock_repo)
    mock_get_mapper.to_response_dto.side_effect = ["resp1", "resp2"]

    result = use_case.execute()

    mock_repo.get_all.assert_called_once()
    assert result == ["resp1", "resp2"]



def test_update_package_success(mock_repo, mock_get_mapper):
    mock_entity = Mock()
    mock_repo.get_by_id.return_value = mock_entity
    use_case = UpdatePackageUseCase(mock_repo)

    dummy_update_dto = Mock(
        descripcion="Tablet Samsung",
        peso=1.2,
        direccion_entrega="Colonia Miramonte Calle 8 Casa 14",
        estado="En tránsito"
    )
    mock_get_mapper.to_response_dto.return_value = "updated_response"

    result = use_case.execute("PKG-001", dummy_update_dto)

    mock_entity.update_info.assert_called_once_with(
        "Tablet Samsung",
        1.2,
        "Colonia Miramonte Calle 8 Casa 14",
        "En tránsito"
    )
    mock_repo.save.assert_called_once_with(mock_entity)
    assert result == "updated_response"

def test_update_package_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None
    use_case = UpdatePackageUseCase(mock_repo)
    dummy_update_dto = Mock()

    with pytest.raises(PackageNotFoundError):
        use_case.execute("PKG-999", dummy_update_dto)

    mock_repo.save.assert_not_called()



def test_delete_package_success(mock_repo):
    mock_repo.get_by_id.return_value = "existing_package"
    use_case = DeletePackageUseCase(mock_repo)

    use_case.execute("PKG-001")

    mock_repo.delete.assert_called_once_with("PKG-001")

def test_delete_package_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None
    use_case = DeletePackageUseCase(mock_repo)

    with pytest.raises(PackageNotFoundError):
        use_case.execute("PKG-999")

    mock_repo.delete.assert_not_called()
