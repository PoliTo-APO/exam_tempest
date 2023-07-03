from tempest.simulation import TempestSimulator
from tempest.errors import SimulationException


def main():
    print("------------------------- R1 -------------------------")
    ts = TempestSimulator()

    ts.add_city("Torino", 125, 8)
    ts.add_village("Avigliana", 50, 5)

    city = ts.get_location("Torino")
    village = ts.get_location("Avigliana")

    print([city.name, city.value, city.resilience])             # ['Torino', 125, 8]
    print([village.name, village.value, village.resilience])    # ['Avigliana', 50, 5]
    print(str(city))                                            # City Torino
    print(str(village))                                         # Village Avigliana

    print("------------------------- R2 -------------------------")
    try:
        city.simulate_damage(9)
        # Missing damage function for city correctly identified
        print("[ERROR] failed to detect missing damage function for city")
    except SimulationException:
        print("Missing damage function for city correctly identified")

    city.set_damage_function(lambda x: x/20)
    try:
        village.set_damage_function(lambda x: x)
        # Setting of damage function on village correctly identified
        print("[ERROR] failed to detect setting of damage function on village")
    except SimulationException:
        print("Setting of damage function on village correctly identified")

    print(city.simulate_damage(9))  # 56.25
    print(city.simulate_damage(8))  # 0

    print(village.simulate_damage(6))   # 5
    print(village.simulate_damage(4))   # 0

    print("------------------------- R3 -------------------------")
    ts.add_city("Racconigi", 90, 7)

    ts.set_next("Avigliana", "Racconigi", 0.5)
    ts.set_next("Torino", "Avigliana", 0.5)

    next_loc, attenuation = ts.get_next("Avigliana")
    print(next_loc.name, attenuation)                # Racconigi 0.5
    next_loc, attenuation = ts.get_next("Torino")
    print(next_loc.name, attenuation)                # Avigliana 0.5
    print(ts.get_next("Racconigi"))                  # None

    print("------------------------- R4 -------------------------")
    city = ts.get_location("Racconigi")
    city.set_damage_function(lambda x: x / 20)

    print([loc.name for loc in ts.get_affected("Torino")])      # ['Torino', 'Avigliana', 'Racconigi']
    print([loc.name for loc in ts.get_affected("Avigliana")])   # ['Avigliana', 'Racconigi']

    print(ts.get_total_damage("Torino", 10))    # 62.5
    print(ts.get_total_damage("Avigliana", 6))  # 5

    print("------------------------- R5 -------------------------")
    ts.add_village("Usseaux", 33, 3)
    ts.add_city("Savigliano", 25, 9)

    ts.add_location("Usseaux", "Avigliana", 0.7)
    ts.add_location("Savigliano", "Racconigi", 0.3)

    next_loc, attenuation = ts.get_next("Avigliana")
    print(next_loc.name, attenuation)   # Usseaux 0.5

    next_loc, attenuation = ts.get_next("Usseaux")
    print(next_loc.name, attenuation)   # Racconigi 0.7

    next_loc, attenuation = ts.get_next("Racconigi")
    print(next_loc.name, attenuation)   # Savigliano 0.3

    print(ts.get_next("Savigliano"))    # None


if __name__ == "__main__":
    main()




