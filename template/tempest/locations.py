from abc import ABC, abstractmethod
from typing import Callable


class Location(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def value(self) -> int:
        pass

    @property
    @abstractmethod
    def resilience(self) -> int:
        pass

    @abstractmethod
    def simulate_damage(self, intensity: float) -> float:
        pass

    @abstractmethod
    def set_damage_function(self, damage_function: Callable[[float], float]) -> None:
        pass
