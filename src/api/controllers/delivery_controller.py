from fastapi import APIRouter, status
from typing import List

from src.application.dtos.delivery_dto import DeliveryCreateDTO, DeliveryUpdateDTO, DeliveryResponseDTO

from src.application.use_cases.create_delivery import CreateDeliveryUseCase
from src.application.use_cases.get_delivery import (
    GetDeliveryByIdUseCase,
    GetAllDeliveriesUseCase,
    UpdateDeliveryUseCase,
    DeleteDeliveryUseCase
)

from src.infrastructure.persistence.sqlite_delivery_repository import SQLiteDeliveryRepository

router = APIRouter(prefix="/deliveries", tags=["Entregas"])

repo = SQLiteDeliveryRepository()

@router.post("/", response_model=DeliveryResponseDTO, status_code=status.HTTP_201_CREATED)
def create_delivery(dto: DeliveryCreateDTO):
    """Registra una nueva entrega en el sistema."""
    use_case = CreateDeliveryUseCase(repo)
    return use_case.execute(dto)

@router.get("/", response_model=List[DeliveryResponseDTO])
def get_all_deliveries():
    """Devuelve la lista completa de entregas registradas."""
    use_case = GetAllDeliveriesUseCase(repo)
    return use_case.execute()

@router.get("/{delivery_id}", response_model=DeliveryResponseDTO)
def get_delivery_by_id(delivery_id: str):
    """Busca una entrega específica utilizando su ID."""
    use_case = GetDeliveryByIdUseCase(repo)
    return use_case.execute(delivery_id)

@router.put("/{delivery_id}", response_model=DeliveryResponseDTO)
def update_delivery(delivery_id: str, dto: DeliveryUpdateDTO):
    """Actualiza los datos de una entrega existente."""
    use_case = UpdateDeliveryUseCase(repo)
    return use_case.execute(delivery_id, dto)

@router.delete("/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delivery(delivery_id: str):
    """Elimina una entrega del sistema por su ID."""
    use_case = DeleteDeliveryUseCase(repo)
    use_case.execute(delivery_id)
    return None
