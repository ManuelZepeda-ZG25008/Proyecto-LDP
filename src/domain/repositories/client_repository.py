from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.client import Client

class ClientRepository(ABC):
    """Contrato abstracto para el manejo de persistencia de Clientes."""

    @abstractmethod
    def save(self, client: Client) -> None:
        """Guarda un nuevo cliente o actualiza uno existente."""
        pass

    @abstractmethod
    def get_by_id(self, client_id: str) -> Optional[Client]:
        """Busca un cliente por su ID único. Devuelve None si no existe."""
        pass

    @abstractmethod
    def get_all(self) -> List[Client]:
        """Devuelve una lista con todos los clientes registrados."""
        pass

    @abstractmethod
    def delete(self, client_id: str) -> None:
        """Elimina un cliente del sistema usando su ID."""
        pass