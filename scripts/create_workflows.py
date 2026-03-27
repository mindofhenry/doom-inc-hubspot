import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["HUBSPOT_ACCESS_TOKEN"]
BASE_URL = "https://api.hubapi.com/automation/v3/workflows"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


def create_workflow(payload):
    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    if response.status_code in (200, 201):
        wf = response.json()
        print(f"✓ Created: {wf.get('name')} (id: {wf.get('id')})")
    else:
        print(f"✗ Error: {response.status_code} — {response.text}")


# ─── WORKFLOW 1: SLA Tier 1 Breach Alert ──────────────────────────────────────
# Triggers when a contact is created with SLA Tier = Tier 1 (respond in 1hr)
# Action: creates a high-priority task on the contact
sla_breach_workflow = {
    "name": "DOOM Inc — SLA Tier 1 Breach Alert",
    "type": "DRIP_DELAY",
    "onlyEnrollsManually": False,
    "enrollmentCriteria": {
        "type": "AND",
        "filters": [
            {
                "operator": "EQ",
                "filterFamily": "ContactProperty",
                "property": "sla_tier",
                "value": "Tier 1 (respond in 1hr)",
                "type": "string",
            }
        ],
    },
    "actions": [
        {
            "type": "CREATE_TASK",
            "body": "SLA BREACH — Tier 1 contact uncontacted. Respond within 1 hour.",
            "subject": "SLA BREACH — Tier 1 Lead Uncontacted",
            "taskType": "TODO",
            "priority": "HIGH",
            "forObjectType": "CONTACT",
            "reminders": [1],
        }
    ],
}

# ─── WORKFLOW 2: Post-Conversion Follow-Up ────────────────────────────────────
# Triggers when Lifecycle Stage changes to Customer
# Action: creates a follow-up task due in 3 days
post_conversion_workflow = {
    "name": "DOOM Inc — Post-Conversion Follow-Up",
    "type": "DRIP_DELAY",
    "onlyEnrollsManually": False,
    "enrollmentCriteria": {
        "type": "AND",
        "filters": [
            {
                "operator": "EQ",
                "filterFamily": "ContactProperty",
                "property": "lifecyclestage",
                "value": "customer",
                "type": "string",
            }
        ],
    },
    "actions": [
        {
            "type": "DELAY",
            "delayMillis": 0,
        },
        {
            "type": "CREATE_TASK",
            "body": "Contact converted. Schedule discovery call within 3 days.",
            "subject": "Post-Conversion Follow-Up — Schedule Discovery Call",
            "taskType": "TODO",
            "priority": "HIGH",
            "forObjectType": "CONTACT",
            "reminders": [259200000],  # 3 days in ms
        },
    ],
}

# ─── WORKFLOW 3: GTM Segment Routing Tag ──────────────────────────────────────
# Triggers when GTM Segment = Enterprise and GTM Persona = CISO or VP of Security
# Action: sets Last Touched By = AE (signals this contact should go to AE queue)
# Note: direct owner assignment requires Operations Hub paid tier.
# This workflow demonstrates the routing logic using a property flag instead.
enterprise_routing_workflow = {
    "name": "DOOM Inc — Enterprise Exec Routing (AE Tag)",
    "type": "DRIP_DELAY",
    "onlyEnrollsManually": False,
    "enrollmentCriteria": {
        "type": "AND",
        "filters": [
            {
                "operator": "EQ",
                "filterFamily": "ContactProperty",
                "property": "gtm_segment",
                "value": "Enterprise",
                "type": "string",
            },
            {
                "operator": "IN",
                "filterFamily": "ContactProperty",
                "property": "gtm_persona",
                "values": ["CISO", "VP of Security"],
                "type": "string",
            },
        ],
    },
    "actions": [
        {
            "type": "SET_CONTACT_PROPERTY",
            "propertyName": "last_touched_by",
            "newValue": "AE",
        }
    ],
}


if __name__ == "__main__":
    print("Creating DOOM Inc workflows...\n")
    create_workflow(sla_breach_workflow)
    create_workflow(post_conversion_workflow)
    create_workflow(enterprise_routing_workflow)
    print("\nDone.")