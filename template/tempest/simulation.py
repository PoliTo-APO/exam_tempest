from tempest.locations import Location
from typing import Tuple, List, Optional


class TempestSimulator:
    def __init__(self):
        pass

    # R1
    def add_village(self, name: str, value: int, resilience: int) -> None:
        pass

    def add_city(self, name: str, value: int, resilience: int) -> None:
        pass

    def get_location(self, name: str) -> Location:
        pass

    # R3
    def set_next(self, location: str, next_location: str, attenuation: float) -> None:
        pass

    def get_next(self, location: str) -> Optional[Tuple[Location, float]]:
        pass

    # R4
    def get_affected(self, start_location: str) -> List[Location]:
        pass

    def get_total_damage(self, start_location: str, intensity: float) -> float:
        pass

    # R5
    def add_location(self, to_insert: str, location_before: str, attenuation: float) -> None:
        pass
