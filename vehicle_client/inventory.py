import json


def load_vehicles():

    with open("data/vehicles.json", "r") as file:
        return json.load(file)


if __name__ == "__main__":

    vehicles = load_vehicles()

    print("\nVehicle Inventory\n")

    for vehicle in vehicles:
        print(
            f"{vehicle['vin']} | "
            f"{vehicle['model']} | "
            f"Battery={vehicle['battery']}%"
        )