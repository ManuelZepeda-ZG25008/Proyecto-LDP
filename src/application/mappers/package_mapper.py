from src.domain.entities.package import Package
from src.application.dtos.package_dto import (
    PackageCreateDTO,
    PackageResponseDTO
)


class PackageMapper:

    @staticmethod
    def to_entity(dto: PackageCreateDTO) -> Package:
        return Package(
            id=dto.id,
            descripcion=dto.descripcion,
            peso=dto.peso,
            destinatario_id=dto.destinatario_id,
            direccion_entrega=dto.direccion_entrega
        )

    @staticmethod
    def to_response_dto(entity: Package) -> PackageResponseDTO:
        return PackageResponseDTO(
            id=entity.id,
            descripcion=entity.descripcion,
            peso=entity.peso,
            destinatario_id=entity.destinatario_id,
            direccion_entrega=entity.direccion_entrega,
            estado=entity.estado
        )