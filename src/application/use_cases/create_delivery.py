from src.domain.repositories.delivery_repository import DeliveryRepository
from src.application.dtos.delivery_dto import DeliveryCreateDTO, DeliveryResponseDTO
from src.application.mappers.delivery_mapper import DeliveryMapper
from src.domain.exceptions import ResourceAlreadyExistsError

class DeliveryAlreadyExistsError(ResourceAlreadyExistsError):
    """Hereda de ResourceAlreadyExistsError (HTTP 409)."""
    pass

class CreateDeliveryUseCase:
    def __init__(self, repository: DeliveryRepository):
        self.repository = repository

    def execute(self, dto: DeliveryCreateDTO) -> DeliveryResponseDTO:
        # 1. Regla de negocio: Verificar si el ID ya existe en la DB
        existing_delivery = self.repository.get_by_id(dto.id)
        if existing_delivery:
            raise DeliveryAlreadyExistsError(f"La entrega con ID '{dto.id}' ya está registrada.")

        # 2. Mapear de DTO a Entidad pura (aquí también se dispara la validación de dominio)
        delivery_entity = DeliveryMapper.to_entity(dto)

        # 3. Guardar en la base de datos usando los fierros de infraestructura
        self.repository.save(delivery_entity)

        # 4. Retornar la data formateada en el DTO de respuesta
        return DeliveryMapper.to_response_dto(delivery_entity)
