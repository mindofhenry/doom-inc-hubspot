import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["HUBSPOT_ACCESS_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# Pipeline stage IDs — HubSpot free tier default sales pipeline
# Fetch yours with: GET https://api.hubapi.com/crm/v3/pipelines/deals
# These map to: Appointment Scheduled, Qualified To Buy, Presentation Scheduled,
#               Decision Maker Bought In, Contract Sent, Closed Won, Closed Lost
PIPELINE_STAGES = {
    "Prospecting": "appointmentscheduled",
    "Discovery": "qualifiedtobuy",
    "Demo": "presentationscheduled",
    "Proposal": "decisionmakerboughtin",
    "Contract Sent": "contractsent",
    "Closed Won": "closedwon",
    "Closed Lost": "closedlost",
}

DEALS = [
    # Enterprise — high value, early/mid stage
    {"dealname": "Fortress Financial — Enterprise Security Suite", "amount": 185000, "dealstage": "presentationscheduled", "closedate": "2026-06-30", "pipeline": "default"},
    {"dealname": "Vantage Systems — SOC Platform", "amount": 142000, "dealstage": "qualifiedtobuy", "closedate": "2026-05-31", "pipeline": "default"},
    {"dealname": "Meridian Corp — Endpoint Protection", "amount": 220000, "dealstage": "decisionmakerboughtin", "closedate": "2026-04-30", "pipeline": "default"},
    {"dealname": "Axiom Logistics — Compliance Package", "amount": 98000, "dealstage": "appointmentscheduled", "closedate": "2026-07-31", "pipeline": "default"},
    {"dealname": "Redwood Capital — Threat Intelligence", "amount": 76000, "dealstage": "qualifiedtobuy", "closedate": "2026-06-15", "pipeline": "default"},
    {"dealname": "Halcyon Industries — OT Security", "amount": 310000, "dealstage": "contractsent", "closedate": "2026-04-15", "pipeline": "default"},
    # Mid-Market — smaller ACV, mixed stages
    {"dealname": "Stratus Tech — SMB Security Bundle", "amount": 38000, "dealstage": "presentationscheduled", "closedate": "2026-05-15", "pipeline": "default"},
    {"dealname": "PineCrest Software — Dev Security", "amount": 24000, "dealstage": "qualifiedtobuy", "closedate": "2026-06-30", "pipeline": "default"},
    {"dealname": "Bridgepoint Analytics — Data Protection", "amount": 31000, "dealstage": "appointmentscheduled", "closedate": "2026-07-15", "pipeline": "default"},
    {"dealname": "Clearwave Solutions — Vulnerability Mgmt", "amount": 18500, "dealstage": "appointmentscheduled", "closedate": "2026-08-31", "pipeline": "default"},
    {"dealname": "Corex Ventures — Identity Security", "amount": 42000, "dealstage": "decisionmakerboughtin", "closedate": "2026-04-30", "pipeline": "default"},
    {"dealname": "Sentinel Systems — Incident Response", "amount": 29000, "dealstage": "qualifiedtobuy", "closedate": "2026-06-15", "pipeline": "default"},
    # Strategic — largest ACV, high-touch
    {"dealname": "Titan Global — Enterprise Platform", "amount": 780000, "dealstage": "contractsent", "closedate": "2026-04-01", "pipeline": "default"},
    {"dealname": "Summit Enterprises — Global SOC", "amount": 540000, "dealstage": "decisionmakerboughtin", "closedate": "2026-05-01", "pipeline": "default"},
    {"dealname": "Horizon Dynamics — Zero Trust", "amount": 410000, "dealstage": "presentationscheduled", "closedate": "2026-06-01", "pipeline": "default"},
    {"dealname": "NorthBridge Group — Risk Platform", "amount": 290000, "dealstage": "qualifiedtobuy", "closedate": "2026-07-01", "pipeline": "default"},
    {"dealname": "Ironclad Defense — SIEM Integration", "amount": 620000, "dealstage": "contractsent", "closedate": "2026-04-15", "pipeline": "default"},
    {"dealname": "VaultWorks — Cloud Security", "amount": 480000, "dealstage": "presentationscheduled", "closedate": "2026-05-15", "pipeline": "default"},
    # Closed
    {"dealname": "Stratus Tech — Pilot → Expansion", "amount": 55000, "dealstage": "closedwon", "closedate": "2026-02-28", "pipeline": "default"},
    {"dealname": "Unknown Industries — SMB Trial", "amount": 5000, "dealstage": "closedlost", "closedate": "2026-01-31", "pipeline": "default"},
]


def create_deals():
    created = 0
    skipped = 0
    errors = 0

    for deal in DEALS:
        response = requests.post(
            "https://api.hubapi.com/crm/v3/objects/deals",
            headers=HEADERS,
            json={"properties": deal}
        )

        if response.status_code in (200, 201):
            print(f"✓ Created: {deal['dealname']} (${deal['amount']:,})")
            created += 1
        elif response.status_code == 409:
            print(f"  Skipped (already exists): {deal['dealname']}")
            skipped += 1
        else:
            print(f"✗ Error creating {deal['dealname']}: {response.status_code} — {response.text}")
            errors += 1

    print(f"\nDone. Created: {created} | Skipped: {skipped} | Errors: {errors}")


if __name__ == "__main__":
    print("Creating DOOM Inc deals...\n")
    create_deals()
