from fastapi import APIRouter, status
from typing import List

# Importamos las estructuras de datos (DTOs)
from src.application.dtos.client_dto import ClientCreateDTO, ClientUpdateDTO, ClientResponseDTO

from src.application.use_cases.create_client import CreateClientUseCase
from src.application.use_cases.get_client import (
    GetClientByIdUseCase, 
    GetAllClientsUseCase, 
    UpdateClientUseCase, 
    DeleteClientUseCase
)

from src.infrastructure.persistence.sqlite_client_repository import SQLiteClientRepository

router = APIRouter(prefix="/clients", tags=["Clientes"])

repo = SQLiteClientRepository()

@router.post("/", response_model=ClientResponseDTO, status_code=status.HTTP_201_CREATED)
def create_client(dto: ClientCreateDTO):
    """Crea un nuevo cliente en el sistema."""
    use_case = CreateClientUseCase(repo)
    return use_case.execute(dto)

@router.get("/", response_model=List[ClientResponseDTO])
def get_all_clients():
    """Devuelve la lista completa de clientes registrados."""
    use_case = GetAllClientsUseCase(repo)
    return use_case.execute()

@router.get("/{client_id}", response_model=ClientResponseDTO)
def get_client_by_id(client_id: str):
    """Busca un cliente específico utilizando su ID."""
    use_case = GetClientByIdUseCase(repo)
    return use_case.execute(client_id)

@router.put("/{client_id}", response_model=ClientResponseDTO)
def update_client(client_id: str, dto: ClientUpdateDTO):
    """Actualiza los datos de un cliente existente."""
    use_case = UpdateClientUseCase(repo)
    return use_case.execute(client_id, dto)

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: str):
    """Elimina un cliente del sistema por su ID."""
    use_case = DeleteClientUseCase(repo)
    use_case.execute(client_id)
    return None