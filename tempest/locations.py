from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional
from tempest.errors import SimulationException


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


class UrbanLocation(Location):
    def __init__(self, name: str, value: int, resilience: int):
        self._name = name
        self._value = value
        self._resilience = resilience
        self._next_location = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> int:
        return self._value

    @property
    def resilience(self) -> int:
        return self._resilience

    @abstractmethod
    def simulate_damage(self, intensity: float) -> float:
        pass

    @abstractmethod
    def set_damage_function(self, damage_function: Callable[[float], float]):
        pass

    @property
    def next_location(self) -> Optional[Tuple[Location, float]]:
        return self._next_location

    @next_location.setter
    def next_location(self, next_location: Tuple[Location, float]):
        self._next_location = next_location


class Village(UrbanLocation):
    def __str__(self):
        return "{} {}".format("Village", self.name)

    def simulate_damage(self, intensity: float) -> float:
        intensity -= self._resilience
        intensity = intensity if intensity > 0 else 0
        return intensity/10 * self.value

    def set_damage_function(self, damage_function: Callable[[float], float]):
        raise SimulationException("Village does not support damage function")


class City(UrbanLocation):
    def __init__(self, name: str, value: int, resilience: int):
        super().__init__(name, value, resilience)
        self._damage_function = None

    def __str__(self):
        return "{} {}".format("City", self.name)

    def simulate_damage(self, intensity: float) -> float:
        if self._damage_function is None:
            raise SimulationException("Damage function not provided")
        if intensity <= self.resilience:
            return 0
        return self.value * self._damage_function(intensity)

    def set_damage_function(self, damage_function: Callable[[float], float]):
        self._damage_function = damage_function
