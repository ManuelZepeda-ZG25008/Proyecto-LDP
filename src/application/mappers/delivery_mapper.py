from src.domain.entities.delivery import Delivery
from src.application.dtos.delivery_dto import DeliveryCreateDTO, DeliveryResponseDTO

class DeliveryMapper:
    """Convierte entre DTOs y la entidad pura de dominio Delivery."""

    @staticmethod
    def to_entity(dto: DeliveryCreateDTO) -> Delivery:
        """Convierte un DeliveryCreateDTO en una entidad de dominio Delivery."""
        return Delivery(
            id=dto.id,
            package_id=dto.package_id,
            client_id=dto.client_id,
            direccion_destino=dto.direccion_destino,
            estado=dto.estado,
            fecha_entrega_estimada=dto.fecha_entrega_estimada,
            notas=dto.notas
        )

    @staticmethod
    def to_response_dto(delivery: Delivery) -> DeliveryResponseDTO:
        """Convierte una entidad de dominio Delivery en un DeliveryResponseDTO."""
        return DeliveryResponseDTO(
            id=delivery.id,
            package_id=delivery.package_id,
            client_id=delivery.client_id,
            direccion_destino=delivery.direccion_destino,
            estado=delivery.estado,
            fecha_entrega_estimada=delivery.fecha_entrega_estimada,
            notas=delivery.notas
        )
