import os
from dotenv import load_dotenv
from hubspot import HubSpot
from hubspot.crm.properties import PropertyCreate
from hubspot.crm.properties.exceptions import ApiException

load_dotenv()

client = HubSpot(access_token=os.environ["HUBSPOT_ACCESS_TOKEN"])

PROPERTIES = [
    {
        "name": "gtm_segment",
        "label": "GTM Segment",
        "type": "enumeration",
        "field_type": "select",
        "options": [
            {"label": "Enterprise", "value": "Enterprise", "displayOrder": 0, "hidden": False},
            {"label": "Mid-Market", "value": "Mid-Market", "displayOrder": 1, "hidden": False},
            {"label": "Strategic", "value": "Strategic", "displayOrder": 2, "hidden": False},
        ],
    },
    {
        "name": "gtm_persona",
        "label": "GTM Persona",
        "type": "enumeration",
        "field_type": "select",
        "options": [
            {"label": "CISO", "value": "CISO", "displayOrder": 0, "hidden": False},
            {"label": "VP of Security", "value": "VP of Security", "displayOrder": 1, "hidden": False},
            {"label": "IT Director", "value": "IT Director", "displayOrder": 2, "hidden": False},
            {"label": "Security Engineer", "value": "Security Engineer", "displayOrder": 3, "hidden": False},
            {"label": "Other", "value": "Other", "displayOrder": 4, "hidden": False},
        ],
    },
    {
        "name": "icp_fit",
        "label": "ICP Fit",
        "type": "enumeration",
        "field_type": "select",
        "options": [
            {"label": "Strong", "value": "Strong", "displayOrder": 0, "hidden": False},
            {"label": "Moderate", "value": "Moderate", "displayOrder": 1, "hidden": False},
            {"label": "Weak", "value": "Weak", "displayOrder": 2, "hidden": False},
            {"label": "Unqualified", "value": "Unqualified", "displayOrder": 3, "hidden": False},
        ],
    },
    {
        "name": "sla_tier",
        "label": "SLA Tier",
        "type": "enumeration",
        "field_type": "select",
        "options": [
            {"label": "Tier 1 (respond in 1hr)", "value": "Tier 1 (respond in 1hr)", "displayOrder": 0, "hidden": False},
            {"label": "Tier 2 (4hr)", "value": "Tier 2 (4hr)", "displayOrder": 1, "hidden": False},
            {"label": "Tier 3 (24hr)", "value": "Tier 3 (24hr)", "displayOrder": 2, "hidden": False},
        ],
    },
    {
        "name": "lead_score",
        "label": "Lead Score",
        "type": "number",
        "field_type": "number",
        "options": [],
    },
    {
        "name": "outbound_sequence",
        "label": "Outbound Sequence",
        "type": "string",
        "field_type": "text",
        "options": [],
    },
    {
        "name": "last_touched_by",
        "label": "Last Touched By",
        "type": "enumeration",
        "field_type": "select",
        "options": [
            {"label": "SDR", "value": "SDR", "displayOrder": 0, "hidden": False},
            {"label": "AE", "value": "AE", "displayOrder": 1, "hidden": False},
            {"label": "Marketing", "value": "Marketing", "displayOrder": 2, "hidden": False},
            {"label": "Partner", "value": "Partner", "displayOrder": 3, "hidden": False},
        ],
    },
]


def create_properties():
    for prop in PROPERTIES:
        try:
            property_def = PropertyCreate(
                name=prop["name"],
                label=prop["label"],
                type=prop["type"],
                field_type=prop["field_type"],
                group_name="contactinformation",
                options=prop["options"],
            )
            client.crm.properties.core_api.create(
                object_type="contacts",
                property_create=property_def,
            )
            print(f"✓ Created: {prop['label']}")
        except ApiException as e:
            if "already exists" in str(e).lower() or "conflict" in str(e).lower():
                print(f"  Skipped (already exists): {prop['label']}")
            else:
                print(f"✗ Error creating {prop['label']}: {e}")


if __name__ == "__main__":
    create_properties()