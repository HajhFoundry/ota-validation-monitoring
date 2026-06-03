import json

from vehicle_client.eligibility_rules import evaluate_eligibility
from vehicle_client.safety_rules import evaluate_safety
from vehicle_client.cybersecurity_rules import evaluate_cybersecurity

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

            eligible, eligibility_reasons = evaluate_eligibility(vehicle, campaign)

            if not eligible:
                print(
                    f"  {vehicle['vin']} -> TARGETED BUT ELIGIBILITY BLOCKED "
                    f"({', '.join(eligibility_reasons)})"
                )
                continue

    

            safe, safety_reasons = evaluate_safety(vehicle, campaign)

            if not safe:
                print(
                    f"  {vehicle['vin']} -> TARGETED BUT SAFETY BLOCKED "
                    f"({', '.join(safety_reasons)})"
                )
                continue

            

            secure, security_reasons = evaluate_cybersecurity(vehicle)

            if not secure:
                print(
                    f"  {vehicle['vin']} -> TARGETED BUT CYBERSECURITY BLOCKED "
                    f"({', '.join(security_reasons)})"
                )
                continue

            print(
                f"  {vehicle['vin']} -> ELIGIBLE + SAFE + CYBERSECURE"
            )


if __name__ == "__main__":
    evaluate_campaigns()