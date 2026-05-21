from typing import List
from src.domain.repositories.delivery_repository import DeliveryRepository
from src.application.dtos.delivery_dto import DeliveryResponseDTO, DeliveryUpdateDTO
from src.application.mappers.delivery_mapper import DeliveryMapper
from src.domain.exceptions import ResourceNotFoundError

class DeliveryNotFoundError(ResourceNotFoundError):
    """Hereda de ResourceNotFoundError (HTTP 404)."""
    pass

class GetDeliveryByIdUseCase:
    def __init__(self, repository: DeliveryRepository):
        self.repository = repository

    def execute(self, delivery_id: str) -> DeliveryResponseDTO:
        delivery = self.repository.get_by_id(delivery_id)
        if not delivery:
            raise DeliveryNotFoundError(f"La entrega con ID '{delivery_id}' no existe.")
        return DeliveryMapper.to_response_dto(delivery)

class GetAllDeliveriesUseCase:
    def __init__(self, repository: DeliveryRepository):
        self.repository = repository

    def execute(self) -> List[DeliveryResponseDTO]:
        deliveries = self.repository.get_all()
        return [DeliveryMapper.to_response_dto(delivery) for delivery in deliveries]

class UpdateDeliveryUseCase:
    def __init__(self, repository: DeliveryRepository):
        self.repository = repository

    def execute(self, delivery_id: str, dto: DeliveryUpdateDTO) -> DeliveryResponseDTO:
        # 1. Buscar si la entrega existe para poder actualizarla
        delivery = self.repository.get_by_id(delivery_id)
        if not delivery:
            raise DeliveryNotFoundError(f"No se puede actualizar. La entrega '{delivery_id}' no existe.")

        # 2. Modificar la info usando el método seguro de la entidad de dominio (auto-valida)
        delivery.update_info(
            direccion_destino=dto.direccion_destino,
            estado=dto.estado,
            fecha_entrega_estimada=dto.fecha_entrega_estimada,
            notas=dto.notas
        )

        # 3. Guardar los cambios en la infraestructura (SQLite hará el REPLACE)
        self.repository.save(delivery)

        return DeliveryMapper.to_response_dto(delivery)

class DeleteDeliveryUseCase:
    def __init__(self, repository: DeliveryRepository):
        self.repository = repository

    def execute(self, delivery_id: str) -> None:
        delivery = self.repository.get_by_id(delivery_id)
        if not delivery:
            raise DeliveryNotFoundError(f"No se puede eliminar. La entrega '{delivery_id}' no existe.")

        self.repository.delete(delivery_id)
