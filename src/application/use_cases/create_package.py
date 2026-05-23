from src.domain.repositories.package_repository import PackageRepository
from src.domain.exceptions import ResourceAlreadyExistsError

from src.application.dtos.package_dto import (
    PackageCreateDTO,
    PackageResponseDTO
)

from src.application.mappers.package_mapper import PackageMapper


class PackageAlreadyExistsError(ResourceAlreadyExistsError):
    pass


class CreatePackageUseCase:

    def __init__(self, repository: PackageRepository):
        self.repository = repository

    def execute(self, dto: PackageCreateDTO) -> PackageResponseDTO:

        existing = self.repository.get_by_id(dto.id)

        if existing:
            raise PackageAlreadyExistsError(
                f"El paquete con ID '{dto.id}' ya existe."
            )

        package = PackageMapper.to_entity(dto)

        self.repository.save(package)

        return PackageMapper.to_response_dto(package)