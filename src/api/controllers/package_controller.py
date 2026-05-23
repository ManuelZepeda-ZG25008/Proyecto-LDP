from fastapi import APIRouter, status
from typing import List

from src.application.dtos.package_dto import (
    PackageCreateDTO,
    PackageUpdateDTO,
    PackageResponseDTO
)

from src.application.use_cases.create_package import (
    CreatePackageUseCase
)

from src.application.use_cases.get_package import (
    GetPackageByIdUseCase,
    GetAllPackagesUseCase,
    UpdatePackageUseCase,
    DeletePackageUseCase
)

from src.infrastructure.persistence.sqlite_package_repository import (
    SQLitePackageRepository
)

router = APIRouter(
    prefix="/packages",
    tags=["Paquetes"]
)

repo = SQLitePackageRepository()


@router.post(
    "/",
    response_model=PackageResponseDTO,
    status_code=status.HTTP_201_CREATED
)
def create_package(dto: PackageCreateDTO):

    use_case = CreatePackageUseCase(repo)

    return use_case.execute(dto)


@router.get(
    "/",
    response_model=List[PackageResponseDTO]
)
def get_all_packages():

    use_case = GetAllPackagesUseCase(repo)

    return use_case.execute()


@router.get(
    "/{package_id}",
    response_model=PackageResponseDTO
)
def get_package_by_id(package_id: str):

    use_case = GetPackageByIdUseCase(repo)

    return use_case.execute(package_id)


@router.put(
    "/{package_id}",
    response_model=PackageResponseDTO
)
def update_package(
    package_id: str,
    dto: PackageUpdateDTO
):

    use_case = UpdatePackageUseCase(repo)

    return use_case.execute(package_id, dto)


@router.delete(
    "/{package_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_package(package_id: str):

    use_case = DeletePackageUseCase(repo)

    use_case.execute(package_id)

    return None