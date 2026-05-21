
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.delivery import Delivery

class DeliveryRepository(ABC):
    """Contrato abstracto para el manejo de persistencia de Entregas."""

    @abstractmethod
    def save(self, delivery: Delivery) -> None:
        """Guarda una nueva entrega o actualiza una existente."""
        pass

    @abstractmethod
    def get_by_id(self, delivery_id: str) -> Optional[Delivery]:
        """Busca una entrega por su ID único. Devuelve None si no existe."""
        pass

    @abstractmethod
    def get_all(self) -> List[Delivery]:
        """Devuelve una lista con todas las entregas registradas."""
        pass

    @abstractmethod
    def delete(self, delivery_id: str) -> None:
        """Elimina una entrega del sistema usando su ID."""
        pass
