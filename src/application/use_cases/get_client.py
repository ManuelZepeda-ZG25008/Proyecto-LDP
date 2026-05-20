from typing import List
from src.domain.repositories.client_repository import ClientRepository
from src.application.dtos.client_dto import ClientResponseDTO, ClientUpdateDTO
from src.application.mappers.client_mapper import ClientMapper
# src/application/use_cases/get_client.py
from src.domain.exceptions import ResourceNotFoundError

class ClientNotFoundError(ResourceNotFoundError):
    """Hereda de ResourceNotFoundError (HTTP 404)."""
    pass

class GetClientByIdUseCase:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def execute(self, client_id: str) -> ClientResponseDTO:
        client = self.repository.get_by_id(client_id)
        if not client:
            raise ClientNotFoundError(f"El cliente con ID '{client_id}' no existe.")
        return ClientMapper.to_response_dto(client)

class GetAllClientsUseCase:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def execute(self) -> List[ClientResponseDTO]:
        clients = self.repository.get_all()
        return [ClientMapper.to_response_dto(client) for client in clients]

class UpdateClientUseCase:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def execute(self, client_id: str, dto: ClientUpdateDTO) -> ClientResponseDTO:
        # 1. Buscar si el cliente existe para poder actualizarlo
        client = self.repository.get_by_id(client_id)
        if not client:
            raise ClientNotFoundError(f"No se puede actualizar. El cliente '{client_id}' no existe.")
        
        # 2. Modificar la info usando el método seguro de la entidad de dominio (auto-valida)
        client.update_info(
            nombre=dto.nombre,
            apellido=dto.apellido,
            email=dto.email,
            telefono=dto.telefono,
            direccion=dto.direccion
        )
        
        # 3. Guardar los cambios en la infraestructura (SQLite hará el REPLACE)
        self.repository.save(client)
        
        return ClientMapper.to_response_dto(client)

class DeleteClientUseCase:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def execute(self, client_id: str) -> None:
        client = self.repository.get_by_id(client_id)
        if not client:
            raise ClientNotFoundError(f"No se puede eliminar. El cliente '{client_id}' no existe.")
            
        self.repository.delete(client_id)