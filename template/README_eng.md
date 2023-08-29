# Tempest simulator
Stormwatchers need a python software to simulate the behavior of tempests.

Modules and classes should be developed in the *tempest* package. Do not move or rename existing modules and classes, and do not modify method signatures.

In *main.py* there is some simple code, which you can modify, that tests the basic functionality. It provides examples of the main methods and correctness checks.

All exceptions, unless otherwise specified, are of type *SimulationException* defined in the *errors* module.

## R1: Cities and Villages
The abstract class *Location* of the *locations* module represents a place of interest for which we want to evaluate the impact of the storm. It defines the abstract properties:

- ```name(self) -> str```
- ```value(self) -> int```
- ```resilience(self) -> int```

They provide the name, architectural value, and weather resilience of the place of interest, respectively. Consider, without checking it, that the resilience value is always between 1 and 10.

The *TempestSimulator* class of the *simulation* module allows you to define cities and villages.

The ```add_village(self, name: str, value: int, resilience: int) -> None``` method allows you to add a village, specifying its name, architectural value, and resilience against bad weather.

The ```add_city(self, name: str, value: int, resilience: int) -> None``` method allows you to add a city, specifying its name, architectural value, and resilience against bad weather.

The ```get_location(self, name: str) -> Location``` method allows you to obtain the object representing a place of interest given the name.

The ```__str__(self) -> str``` method of *Location* returns a string representation of a place of interest. The string consists of the type of place (*Village* or *City*) followed by its name, separated by a space.
Examples:
- *City Roma*
- *Village Gualtieri*


## R2: Damage calculation
The abstract method ```simulate_damage(self, intensity: float) -> float``` of the *Location* class calculates the damage to the architectural value of a place of interest, given the intensity of the storm that hits it. Consider, without checking it, that the intensity value is always between 1 and 10.

The abstract method ```set_damage_function(self, damage_function: Callable[[float], float]) -> None``` of the class *Location* allows you to set a **damage function** which, receiving the value of the intensity of the storm as a parameter, returns a value between zero and one, representing the percentage of the architectural value that was damaged. This method, if invoked on an object representing a village, must throw an exception.

Damage calculation is different depending on whether the place of interest is a city or a village.

For a village the damage formula is as follows: ```damage = architectural_value * (strength - resilience) / 10```. If the formula produces a negative result, the damage suffered must be zero.

For a city, the damage taken is equal to the percentage returned by the damage function, multiplied by the city's architectural value, **ONLY** if the city's resilience is less than the intensity of the storm. In all other cases, the damages are zero.

In the case a **damage function*** is not set for the city, the ```simulate_damage``` method throws an exception.


## R3: High-risk areas
The *TempestSimulator* class allows you to represent the movements of the storm.

The ```set_next(self, location: str, next_location: str, attenuation: float) -> None``` method accepts the names of two places of interest as the first two parameters, allowing you to specify that, in the event that a storm hits the first, the latter would be the next to be hit.

The storm, moving from one place to another, decreases in intensity. The new intensity will be equal to the intensity in the first place, multiplied by the attenuation factor, provided as the third parameter.

**IMPORTANT:** Consider that each place can have only a single previous location and a single following location.

The method ```get_next(self, location: str) -> Optional[Tuple[Location, float]]```, given the name of a place of interest, returns a tuple containing the object representing the next place hit and the value of the factor of attenuation due to travel between the two locations. If the next place is not defined, the method should return ```None```.

## R4: Simulation

The *TempestSimulator* class allows you to simulate a storm.

The method ```get_affected(self, start_location: str) -> List[Location]``` returns the list of places of interest affected by the storm, given the name of the starting place.

The ```get_total_damage(self, start_location: str, intensity: float)``` method, given the name of the starting location and the intensity of a storm, returns the sum of the architectural damage suffered by the places of interest encountered by the storm along its path.

**CONSIDER THE ATTENUATIUON** of storm intensity as it moves from one location to the next.


## R5: Path changes
A storm can change its path and hit a place that was not foreseen.

The ```add_location(self, to_insert: str, location_before: str, attenuation: float) -> None``` method takes the name of the place of interest to add to the storm path, and the name of the place that precedes it. Insert the place of interest while keeping the portions of the route that follow and precede it unchanged.

**TWO CASES** may occur:

- the place to add is in the middle of the route.
- the place preceding the one to be added is the last of the route.

In the first case, the attenuation of the storm, provided as a third parameter, is the attenuation of the storm when moving to the inserted place to the next one. The other attenuation values **DO NOT** vary.

In the second case, the attenuation value provided as the third parameter is the one suffered by the storm when moving to the last place entered.
