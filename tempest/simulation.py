from tempest.locations import Location, Village, City
from typing import Tuple, List, Optional


class TempestSimulator:
    def __init__(self):
        self._locations = {}

    # R1
    def add_village(self, name: str, value: int, resilience: int) -> None:
        self._locations[name] = Village(name, value, resilience)

    def add_city(self, name: str, value: int, resilience: int) -> None:
        self._locations[name] = City(name, value, resilience)

    def get_location(self, name: str) -> Location:
        return self._locations[name]

    # R3
    def set_next(self, location: str, next_location: str, attenuation: float) -> None:
        self._locations[location].next_location = (self._locations[next_location], attenuation)

    def get_next(self, location: str) -> Optional[Tuple[Location, float]]:
        return self._locations[location].next_location

    # R4
    def get_affected(self, start_location: str) -> List[Location]:
        curr_loc = self._locations[start_location]
        affected = [curr_loc]
        while curr_loc.next_location is not None:
            curr_loc, _ = curr_loc.next_location
            affected.append(curr_loc)
        return affected

    def get_total_damage(self, start_location: str, intensity: float) -> float:
        curr_loc = self._locations[start_location]
        total_damage = curr_loc.simulate_damage(intensity)
        while curr_loc.next_location is not None:
            curr_loc, attenuation = curr_loc.next_location
            intensity = intensity * attenuation
            total_damage += curr_loc.simulate_damage(intensity)
        return total_damage

    # R5
    def add_location(self, to_insert: str, location_before: str, attenuation: float) -> None:
        # get location object
        location_before = self._locations[location_before]
        to_insert = self._locations[to_insert]
        if location_before.next_location is not None:
            after_location, before_intensity = location_before.next_location
            location_before.next_location = (to_insert, before_intensity)
            to_insert.next_location = (after_location, attenuation)
        else:
            location_before.next_location = (to_insert, attenuation)




