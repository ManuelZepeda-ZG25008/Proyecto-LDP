from src.domain.entities.client import Client
from src.application.dtos.client_dto import ClientCreateDTO, ClientResponseDTO

class ClientMapper:
    """Traductor de estructuras entre la capa de API/Aplicación y el Dominio."""
    @staticmethod
    def to_entity(dto: ClientCreateDTO) -> Client:
        """Convierte los datos de creación de la API a una entidad pura de dominio."""
        return Client(
            id=dto.id,
            nombre=dto.nombre,
            apellido=dto.apellido,
            email=dto.email,
            telefono=dto.telefono,
            direccion=dto.direccion
        )

    @staticmethod
    def to_response_dto(entity: Client) -> ClientResponseDTO:
        """Convierte una entidad de dominio a un DTO listo para escupir como JSON."""
        return ClientResponseDTO(
            id=entity.id,
            nombre=entity.nombre,
            apellido=entity.apellido,
            email=entity.email,
            telefono=entity.telefono,
            direccion=entity.direccion
        )