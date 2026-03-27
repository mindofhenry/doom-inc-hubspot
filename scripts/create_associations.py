import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["HUBSPOT_ACCESS_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# Association type IDs (HubSpot defaults)
CONTACT_TO_COMPANY = 279  # contact -> company
CONTACT_TO_DEAL = 4       # contact -> deal


def get_all(object_type, props):
    """Fetch all records of a given type, returning {name/identifier: id}."""
    results = {}
    url = f"https://api.hubapi.com/crm/v3/objects/{object_type}"
    params = {"limit": 100, "properties": ",".join(props)}

    while url:
        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        data = r.json()
        for obj in data.get("results", []):
            p = obj["properties"]
            # Key by the first non-null prop value
            key = next((p[k] for k in props if p.get(k)), None)
            if key:
                results[key] = obj["id"]
        url = data.get("paging", {}).get("next", {}).get("link")
        params = {}  # pagination link already includes params

    return results


def associate(from_type, from_id, to_type, to_id, assoc_type_id):
    url = (
        f"https://api.hubapi.com/crm/v3/objects/{from_type}/{from_id}"
        f"/associations/{to_type}/{to_id}/{assoc_type_id}"
    )
    r = requests.put(url, headers=HEADERS)
    return r.status_code in (200, 201, 204)


# Map: contact email prefix -> company name
CONTACT_TO_COMPANY_MAP = {
    "v.nakamura@fortress.example.com": "Fortress Financial",
    "r.okafor@vantage.example.com": "Vantage Systems",
    "d.castellanos@meridian.example.com": "Meridian Corp",
    "j.price@axiom.example.com": "Axiom Logistics",
    "p.mehta@redwood.example.com": "Redwood Capital",
    "m.tran@halcyon.example.com": "Halcyon Industries",
    "a.burns@stratus.example.com": "Stratus Tech",
    "d.osei@pinecrest.example.com": "PineCrest Software",
    "s.liu@bridgepoint.example.com": "Bridgepoint Analytics",
    "t.ibarra@clearwave.example.com": "Clearwave Solutions",
    "e.vasquez@titan.example.com": "Titan Global",
    "n.fitzgerald@summit.example.com": "Summit Enterprises",
    "k.yamamoto@horizon.example.com": "Horizon Dynamics",
    "a.cole@northbridge.example.com": "NorthBridge Group",
    "c.nguyen@unknown.example.com": "Unknown Industries",
    "b.warren@generic.example.com": "Generic Corp",
    "s.adeyemi@corex.example.com": "Corex Ventures",
    "j.hollis@ironclad.example.com": "Ironclad Defense",
    "k.park@vaultworks.example.com": "VaultWorks",
    "l.okonkwo@sentinel.example.com": "Sentinel Systems",
}

# Map: contact email -> deal name
CONTACT_TO_DEAL_MAP = {
    "v.nakamura@fortress.example.com": "Fortress Financial — Enterprise Security Suite",
    "r.okafor@vantage.example.com": "Vantage Systems — SOC Platform",
    "d.castellanos@meridian.example.com": "Meridian Corp — Endpoint Protection",
    "j.price@axiom.example.com": "Axiom Logistics — Compliance Package",
    "p.mehta@redwood.example.com": "Redwood Capital — Threat Intelligence",
    "m.tran@halcyon.example.com": "Halcyon Industries — OT Security",
    "a.burns@stratus.example.com": "Stratus Tech — SMB Security Bundle",
    "d.osei@pinecrest.example.com": "PineCrest Software — Dev Security",
    "s.liu@bridgepoint.example.com": "Bridgepoint Analytics — Data Protection",
    "t.ibarra@clearwave.example.com": "Clearwave Solutions — Vulnerability Mgmt",
    "e.vasquez@titan.example.com": "Titan Global — Enterprise Platform",
    "n.fitzgerald@summit.example.com": "Summit Enterprises — Global SOC",
    "k.yamamoto@horizon.example.com": "Horizon Dynamics — Zero Trust",
    "a.cole@northbridge.example.com": "NorthBridge Group — Risk Platform",
    "s.adeyemi@corex.example.com": "Corex Ventures — Identity Security",
    "j.hollis@ironclad.example.com": "Ironclad Defense — SIEM Integration",
    "k.park@vaultworks.example.com": "VaultWorks — Cloud Security",
    "l.okonkwo@sentinel.example.com": "Sentinel Systems — Incident Response",
}


def main():
    print("Fetching contacts, companies, and deals...\n")

    contacts = get_all("contacts", ["email"])
    companies = get_all("companies", ["name"])
    deals = get_all("deals", ["dealname"])

    print(f"Found: {len(contacts)} contacts, {len(companies)} companies, {len(deals)} deals\n")

    # ── Contact → Company associations ───────────────────────────────────────
    print("Associating contacts → companies...")
    c2c_ok = 0
    c2c_fail = 0
    for email, company_name in CONTACT_TO_COMPANY_MAP.items():
        contact_id = contacts.get(email)
        company_id = companies.get(company_name)
        if not contact_id:
            print(f"  ✗ Contact not found: {email}")
            c2c_fail += 1
            continue
        if not company_id:
            print(f"  ✗ Company not found: {company_name}")
            c2c_fail += 1
            continue
        if associate("contacts", contact_id, "companies", company_id, CONTACT_TO_COMPANY):
            print(f"  ✓ {email} → {company_name}")
            c2c_ok += 1
        else:
            print(f"  ✗ Failed: {email} → {company_name}")
            c2c_fail += 1

    # ── Contact → Deal associations ───────────────────────────────────────────
    print(f"\nAssociating contacts → deals...")
    c2d_ok = 0
    c2d_fail = 0
    for email, deal_name in CONTACT_TO_DEAL_MAP.items():
        contact_id = contacts.get(email)
        deal_id = deals.get(deal_name)
        if not contact_id:
            print(f"  ✗ Contact not found: {email}")
            c2d_fail += 1
            continue
        if not deal_id:
            print(f"  ✗ Deal not found: {deal_name}")
            c2d_fail += 1
            continue
        if associate("contacts", contact_id, "deals", deal_id, CONTACT_TO_DEAL):
            print(f"  ✓ {email} → {deal_name}")
            c2d_ok += 1
        else:
            print(f"  ✗ Failed: {email} → {deal_name}")
            c2d_fail += 1

    print(f"\nDone.")
    print(f"Contact → Company: {c2c_ok} ok, {c2c_fail} failed")
    print(f"Contact → Deal:    {c2d_ok} ok, {c2d_fail} failed")


if __name__ == "__main__":
    main()
