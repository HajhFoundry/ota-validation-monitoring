import json


def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def is_vehicle_targeted(vehicle, campaign):
    if vehicle["model"] != campaign["target_model"]:
        return False, "Model mismatch"

    if vehicle["year"] != campaign["target_year"]:
        return False, "Year mismatch"

    if vehicle["region"] != campaign["target_region"]:
        return False, "Region mismatch"

    if vehicle["update_type"] != campaign["update_type"]:
        return False, "Update type mismatch"

    return True, "Targeted"


def check_eligibility(vehicle, campaign):
    if vehicle["battery"] < campaign["minimum_battery"]:
        return False, f"Battery too low: {vehicle['battery']}%"

    if campaign["wifi_required"] and not vehicle["wifi_connected"]:
        return False, "WiFi required but not connected"

    if campaign["ignition_required_off"] and vehicle["ignition"]:
        return False, "Ignition must be OFF"

    if campaign["vehicle_must_be_parked"] and vehicle["driving"]:
        return False, "Vehicle must be parked"

    return True, "Eligible"


def evaluate_campaigns():
    vehicles = load_json("data/vehicles.json")
    campaigns = load_json("data/campaigns.json")

    print("\nOTA Campaign Evaluation Report\n")

    for campaign in campaigns:
        print(f"Campaign: {campaign['campaign_id']} - {campaign['campaign_name']}")

        for vehicle in vehicles:
            targeted, target_reason = is_vehicle_targeted(vehicle, campaign)

            if not targeted:
                print(f"  {vehicle['vin']} -> NOT TARGETED ({target_reason})")
                continue

            eligible, eligibility_reason = check_eligibility(vehicle, campaign)

            if eligible:
                print(f"  {vehicle['vin']} -> ELIGIBLE")
            else:
                print(f"  {vehicle['vin']} -> TARGETED BUT BLOCKED ({eligibility_reason})")

        print()


if __name__ == "__main__":
    evaluate_campaigns()