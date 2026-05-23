from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.package import Package


class PackageRepository(ABC):

    @abstractmethod
    def save(self, package: Package) -> None:
        pass

    @abstractmethod
    def get_by_id(self, package_id: str) -> Optional[Package]:
        pass

    @abstractmethod
    def get_all(self) -> List[Package]:
        pass

    @abstractmethod
    def delete(self, package_id: str) -> None:
        pass