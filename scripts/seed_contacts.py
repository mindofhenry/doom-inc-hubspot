import os
from dotenv import load_dotenv
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate
from hubspot.crm.contacts.exceptions import ApiException

load_dotenv()

client = HubSpot(access_token=os.environ["HUBSPOT_ACCESS_TOKEN"])

CONTACTS = [
    # Enterprise + CISO
    {"firstname": "Victoria", "lastname": "Nakamura", "email": "v.nakamura@fortress.example.com", "company": "Fortress Financial", "jobtitle": "CISO", "gtm_segment": "Enterprise", "gtm_persona": "CISO", "sla_tier": "Tier 1 (respond in 1hr)", "icp_fit": "Strong", "lead_score": 92, "outbound_sequence": "ENT-CISO-01"},
    {"firstname": "Raymond", "lastname": "Okafor", "email": "r.okafor@vantage.example.com", "company": "Vantage Systems", "jobtitle": "Chief Information Security Officer", "gtm_segment": "Enterprise", "gtm_persona": "CISO", "sla_tier": "Tier 1 (respond in 1hr)", "icp_fit": "Strong", "lead_score": 88, "outbound_sequence": "ENT-CISO-01"},
    # Enterprise + VP of Security
    {"firstname": "Diane", "lastname": "Castellanos", "email": "d.castellanos@meridian.example.com", "company": "Meridian Corp", "jobtitle": "VP of Security", "gtm_segment": "Enterprise", "gtm_persona": "VP of Security", "sla_tier": "Tier 1 (respond in 1hr)", "icp_fit": "Strong", "lead_score": 85, "outbound_sequence": "ENT-VP-01"},
    {"firstname": "Jonathan", "lastname": "Price", "email": "j.price@axiom.example.com", "company": "Axiom Logistics", "jobtitle": "VP Security & Compliance", "gtm_segment": "Enterprise", "gtm_persona": "VP of Security", "sla_tier": "Tier 2 (4hr)", "icp_fit": "Moderate", "lead_score": 74, "outbound_sequence": "ENT-VP-01"},
    # Enterprise + Other Persona
    {"firstname": "Priya", "lastname": "Mehta", "email": "p.mehta@redwood.example.com", "company": "Redwood Capital", "jobtitle": "IT Director", "gtm_segment": "Enterprise", "gtm_persona": "IT Director", "sla_tier": "Tier 2 (4hr)", "icp_fit": "Moderate", "lead_score": 68, "outbound_sequence": "ENT-GEN-01"},
    {"firstname": "Marcus", "lastname": "Tran", "email": "m.tran@halcyon.example.com", "company": "Halcyon Industries", "jobtitle": "Security Engineer", "gtm_segment": "Enterprise", "gtm_persona": "Security Engineer", "sla_tier": "Tier 3 (24hr)", "icp_fit": "Weak", "lead_score": 41, "outbound_sequence": "ENT-GEN-01"},
    # Mid-Market
    {"firstname": "Alicia", "lastname": "Burns", "email": "a.burns@stratus.example.com", "company": "Stratus Tech", "jobtitle": "IT Director", "gtm_segment": "Mid-Market", "gtm_persona": "IT Director", "sla_tier": "Tier 1 (respond in 1hr)", "icp_fit": "Strong", "lead_score": 80, "outbound_sequence": "MM-01"},
    {"firstname": "Derek", "lastname": "Osei", "email": "d.osei@pinecrest.example.com", "company": "PineCrest Software", "jobtitle": "CISO", "gtm_segment": "Mid-Market", "gtm_persona": "CISO", "sla_tier": "Tier 2 (4hr)", "icp_fit": "Moderate", "lead_score": 63, "outbound_sequence": "MM-01"},
    {"firstname": "Samantha", "lastname": "Liu", "email": "s.liu@bridgepoint.example.com", "company": "Bridgepoint Analytics", "jobtitle": "VP of Security", "gtm_segment": "Mid-Market", "gtm_persona": "VP of Security", "sla_tier": "Tier 2 (4hr)", "icp_fit": "Moderate", "lead_score": 57, "outbound_sequence": "MM-01"},
    {"firstname": "Tom", "lastname": "Ibarra", "email": "t.ibarra@clearwave.example.com", "company": "Clearwave Solutions", "jobtitle": "Security Engineer", "gtm_segment": "Mid-Market", "gtm_persona": "Security Engineer", "sla_tier": "Tier 3 (24hr)", "icp_fit": "Weak", "lead_score": 32, "outbound_sequence": "MM-01"},
    # Strategic
    {"firstname": "Elena", "lastname": "Vasquez", "email": "e.vasquez@titan.example.com", "company": "Titan Global", "jobtitle": "CISO", "gtm_segment": "Strategic", "gtm_persona": "CISO", "sla_tier": "Tier 1 (respond in 1hr)", "icp_fit": "Strong", "lead_score": 95, "outbound_sequence": "STRAT-01"},
    {"firstname": "Noah", "lastname": "Fitzgerald", "email": "n.fitzgerald@summit.example.com", "company": "Summit Enterprises", "jobtitle": "VP of Security", "gtm_segment": "Strategic", "gtm_persona": "VP of Security", "sla_tier": "Tier 1 (respond in 1hr)", "icp_fit": "Strong", "lead_score": 91, "outbound_sequence": "STRAT-01"},
    {"firstname": "Keiko", "lastname": "Yamamoto", "email": "k.yamamoto@horizon.example.com", "company": "Horizon Dynamics", "jobtitle": "IT Director", "gtm_segment": "Strategic", "gtm_persona": "IT Director", "sla_tier": "Tier 2 (4hr)", "icp_fit": "Moderate", "lead_score": 72, "outbound_sequence": "STRAT-01"},
    {"firstname": "Adrian", "lastname": "Cole", "email": "a.cole@northbridge.example.com", "company": "NorthBridge Group", "jobtitle": "Security Engineer", "gtm_segment": "Strategic", "gtm_persona": "Security Engineer", "sla_tier": "Tier 3 (24hr)", "icp_fit": "Unqualified", "lead_score": 18, "outbound_sequence": "STRAT-01"},
    # Default catch-all
    {"firstname": "Carl", "lastname": "Nguyen", "email": "c.nguyen@unknown.example.com", "company": "Unknown Industries", "jobtitle": "Other", "gtm_segment": "", "gtm_persona": "Other", "sla_tier": "Tier 3 (24hr)", "icp_fit": "Unqualified", "lead_score": 10, "outbound_sequence": ""},
    {"firstname": "Beth", "lastname": "Warren", "email": "b.warren@generic.example.com", "company": "Generic Corp", "jobtitle": "Manager", "gtm_segment": "", "gtm_persona": "Other", "sla_tier": "Tier 3 (24hr)", "icp_fit": "Unqualified", "lead_score": 5, "outbound_sequence": ""},
    # Mixed high-urgency
    {"firstname": "Simone", "lastname": "Adeyemi", "email": "s.adeyemi@corex.example.com", "company": "Corex Ventures", "jobtitle": "CISO", "gtm_segment": "Mid-Market", "gtm_persona": "CISO", "sla_tier": "Tier 1 (respond in 1hr)", "icp_fit": "Strong", "lead_score": 87, "outbound_sequence": "MM-01"},
    {"firstname": "James", "lastname": "Hollis", "email": "j.hollis@ironclad.example.com", "company": "Ironclad Defense", "jobtitle": "VP of Security", "gtm_segment": "Strategic", "gtm_persona": "VP of Security", "sla_tier": "Tier 1 (respond in 1hr)", "icp_fit": "Strong", "lead_score": 90, "outbound_sequence": "STRAT-01"},
    {"firstname": "Kenji", "lastname": "Park", "email": "k.park@vaultworks.example.com", "company": "VaultWorks", "jobtitle": "CISO", "gtm_segment": "Enterprise", "gtm_persona": "CISO", "sla_tier": "Tier 1 (respond in 1hr)", "icp_fit": "Strong", "lead_score": 93, "outbound_sequence": "ENT-CISO-01"},
    {"firstname": "Layla", "lastname": "Okonkwo", "email": "l.okonkwo@sentinel.example.com", "company": "Sentinel Systems", "jobtitle": "VP of Security", "gtm_segment": "Mid-Market", "gtm_persona": "VP of Security", "sla_tier": "Tier 2 (4hr)", "icp_fit": "Moderate", "lead_score": 61, "outbound_sequence": "MM-01"},
]


def seed_contacts():
    created = 0
    skipped = 0
    errors = 0

    for contact in CONTACTS:
        try:
            properties = {k: str(v) for k, v in contact.items() if v != ""}
            obj = SimplePublicObjectInputForCreate(properties=properties)
            client.crm.contacts.basic_api.create(simple_public_object_input_for_create=obj)
            print(f"✓ Created: {contact['firstname']} {contact['lastname']} — {contact['company']}")
            created += 1
        except ApiException as e:
            if "conflict" in str(e).lower() or "already exists" in str(e).lower():
                print(f"  Skipped (already exists): {contact['email']}")
                skipped += 1
            else:
                print(f"✗ Error creating {contact['email']}: {e}")
                errors += 1

    print(f"\nDone. Created: {created} | Skipped: {skipped} | Errors: {errors}")


if __name__ == "__main__":
    seed_contacts()