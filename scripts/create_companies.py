import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["HUBSPOT_ACCESS_TOKEN"]
BASE_URL = "https://api.hubapi.com/crm/v3/objects/companies"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

COMPANIES = [
    # Enterprise
    {"name": "Fortress Financial", "domain": "fortress.example.com", "industry": "FINANCIAL_SERVICES", "numberofemployees": 3200, "annualrevenue": 180000000, "city": "New York", "state": "NY"},
    {"name": "Vantage Systems", "domain": "vantage.example.com", "industry": "INFORMATION_TECHNOLOGY_AND_SERVICES", "numberofemployees": 1800, "annualrevenue": 95000000, "city": "Chicago", "state": "IL"},
    {"name": "Meridian Corp", "domain": "meridian.example.com", "industry": "INFORMATION_TECHNOLOGY_AND_SERVICES", "numberofemployees": 4500, "annualrevenue": 310000000, "city": "Austin", "state": "TX"},
    {"name": "Axiom Logistics", "domain": "axiom.example.com", "industry": "TRANSPORTATION_TRUCKING_RAILROAD", "numberofemployees": 2100, "annualrevenue": 140000000, "city": "Dallas", "state": "TX"},
    {"name": "Redwood Capital", "domain": "redwood.example.com", "industry": "FINANCIAL_SERVICES", "numberofemployees": 900, "annualrevenue": 75000000, "city": "San Francisco", "state": "CA"},
    {"name": "Halcyon Industries", "domain": "halcyon.example.com", "industry": "INDUSTRIAL_AUTOMATION", "numberofemployees": 5800, "annualrevenue": 420000000, "city": "Detroit", "state": "MI"},
    # Mid-Market
    {"name": "Stratus Tech", "domain": "stratus.example.com", "industry": "INFORMATION_TECHNOLOGY_AND_SERVICES", "numberofemployees": 350, "annualrevenue": 28000000, "city": "Seattle", "state": "WA"},
    {"name": "PineCrest Software", "domain": "pinecrest.example.com", "industry": "COMPUTER_SOFTWARE", "numberofemployees": 180, "annualrevenue": 14000000, "city": "Denver", "state": "CO"},
    {"name": "Bridgepoint Analytics", "domain": "bridgepoint.example.com", "industry": "INFORMATION_TECHNOLOGY_AND_SERVICES", "numberofemployees": 220, "annualrevenue": 19000000, "city": "Boston", "state": "MA"},
    {"name": "Clearwave Solutions", "domain": "clearwave.example.com", "industry": "COMPUTER_SOFTWARE", "numberofemployees": 140, "annualrevenue": 9500000, "city": "Atlanta", "state": "GA"},
    {"name": "Corex Ventures", "domain": "corex.example.com", "industry": "FINANCIAL_SERVICES", "numberofemployees": 95, "annualrevenue": 8000000, "city": "Miami", "state": "FL"},
    {"name": "Sentinel Systems", "domain": "sentinel.example.com", "industry": "SECURITY_AND_INVESTIGATIONS", "numberofemployees": 260, "annualrevenue": 22000000, "city": "Phoenix", "state": "AZ"},
    # Strategic
    {"name": "Titan Global", "domain": "titan.example.com", "industry": "INFORMATION_TECHNOLOGY_AND_SERVICES", "numberofemployees": 12000, "annualrevenue": 980000000, "city": "New York", "state": "NY"},
    {"name": "Summit Enterprises", "domain": "summit.example.com", "industry": "MANAGEMENT_CONSULTING", "numberofemployees": 8500, "annualrevenue": 720000000, "city": "Washington", "state": "DC"},
    {"name": "Horizon Dynamics", "domain": "horizon.example.com", "industry": "INFORMATION_TECHNOLOGY_AND_SERVICES", "numberofemployees": 6200, "annualrevenue": 530000000, "city": "San Jose", "state": "CA"},
    {"name": "NorthBridge Group", "domain": "northbridge.example.com", "industry": "FINANCIAL_SERVICES", "numberofemployees": 3800, "annualrevenue": 290000000, "city": "Minneapolis", "state": "MN"},
    {"name": "Ironclad Defense", "domain": "ironclad.example.com", "industry": "DEFENSE_SPACE", "numberofemployees": 9100, "annualrevenue": 840000000, "city": "Arlington", "state": "VA"},
    {"name": "VaultWorks", "domain": "vaultworks.example.com", "industry": "INFORMATION_TECHNOLOGY_AND_SERVICES", "numberofemployees": 7400, "annualrevenue": 610000000, "city": "Chicago", "state": "IL"},
    # Catch-all
    {"name": "Unknown Industries", "domain": "unknown.example.com", "industry": "COMPUTER_NETWORK_SECURITY", "numberofemployees": 50, "annualrevenue": 2000000, "city": "Unknown", "state": "CA"},
    {"name": "Generic Corp", "domain": "generic.example.com", "industry": "COMPUTER_NETWORK_SECURITY", "numberofemployees": 30, "annualrevenue": 1000000, "city": "Unknown", "state": "CA"},
]


def create_companies():
    created = 0
    skipped = 0
    errors = 0

    for company in COMPANIES:
        properties = {k: str(v) for k, v in company.items()}
        response = requests.post(BASE_URL, headers=HEADERS, json={"properties": properties})

        if response.status_code in (200, 201):
            print(f"✓ Created: {company['name']}")
            created += 1
        elif response.status_code == 409:
            print(f"  Skipped (already exists): {company['name']}")
            skipped += 1
        else:
            print(f"✗ Error creating {company['name']}: {response.status_code} — {response.text}")
            errors += 1

    print(f"\nDone. Created: {created} | Skipped: {skipped} | Errors: {errors}")


if __name__ == "__main__":
    create_companies()
