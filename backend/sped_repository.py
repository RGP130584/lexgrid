from abc import ABC, abstractmethod
from domain.entities.sped import SpedFile


class SpedRepository(ABC):
    @abstractmethod
    def save(self, sped_file: SpedFile) -> bool:
        pass