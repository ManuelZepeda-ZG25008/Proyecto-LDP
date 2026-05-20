from src.domain.repositories.client_repository import ClientRepository
from src.application.dtos.client_dto import ClientCreateDTO, ClientResponseDTO
from src.application.mappers.client_mapper import ClientMapper
from src.domain.exceptions import ResourceAlreadyExistsError

class ClientAlreadyExistsError(ResourceAlreadyExistsError):
    """Hereda de ResourceAlreadyExistsError (HTTP 409)."""
    pass

class CreateClientUseCase:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def execute(self, dto: ClientCreateDTO) -> ClientResponseDTO:
        # 1. Regla de negocio: Verificar si el ID ya existe en la DB
        existing_client = self.repository.get_by_id(dto.id)
        if existing_client:
            raise ClientAlreadyExistsError(f"El cliente con ID '{dto.id}' ya está registrado.")

        # 2. Mapear de DTO a Entidad pura 
        client_entity = ClientMapper.to_entity(dto)

        # 3. Guardar en la base de datos usando los fierros de infraestructura
        self.repository.save(client_entity)

        # 4. Retornar la data formateada en el DTO de respuesta
        return ClientMapper.to_response_dto(client_entity)