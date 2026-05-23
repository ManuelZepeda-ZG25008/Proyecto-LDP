from src.domain.repositories.package_repository import PackageRepository
from src.domain.exceptions import ResourceNotFoundError

from src.application.dtos.package_dto import (
    PackageUpdateDTO,
    PackageResponseDTO
)

from src.application.mappers.package_mapper import PackageMapper


class PackageNotFoundError(ResourceNotFoundError):
    pass


class GetPackageByIdUseCase:

    def __init__(self, repository: PackageRepository):
        self.repository = repository

    def execute(self, package_id: str):

        package = self.repository.get_by_id(package_id)

        if not package:
            raise PackageNotFoundError(
                f"Paquete '{package_id}' no encontrado."
            )

        return PackageMapper.to_response_dto(package)


class GetAllPackagesUseCase:

    def __init__(self, repository: PackageRepository):
        self.repository = repository

    def execute(self):

        packages = self.repository.get_all()

        return [
            PackageMapper.to_response_dto(p)
            for p in packages
        ]


class UpdatePackageUseCase:

    def __init__(self, repository: PackageRepository):
        self.repository = repository

    def execute(self, package_id: str, dto: PackageUpdateDTO):

        package = self.repository.get_by_id(package_id)

        if not package:
            raise PackageNotFoundError(
                f"Paquete '{package_id}' no encontrado."
            )

        package.update_info(
            dto.descripcion,
            dto.peso,
            dto.direccion_entrega,
            dto.estado
        )

        self.repository.save(package)

        return PackageMapper.to_response_dto(package)


class DeletePackageUseCase:

    def __init__(self, repository: PackageRepository):
        self.repository = repository

    def execute(self, package_id: str):

        package = self.repository.get_by_id(package_id)

        if not package:
            raise PackageNotFoundError(
                f"Paquete '{package_id}' no encontrado."
            )

        self.repository.delete(package_id)