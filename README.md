# DOOM Inc — HubSpot GTM Org Build

A HubSpot CRM portfolio project simulating the revenue operations infrastructure of a fictional B2B cybersecurity company. Built to demonstrate GTM systems design: custom data modeling, contact/company/deal architecture, automation design, and API-driven org setup.

---

## What This Is

DOOM Inc (Defensive Operations & Monitoring) is a mock Series B security SaaS targeting enterprise, mid-market, and strategic accounts. This repo contains Python scripts that programmatically build their HubSpot CRM from scratch — the kind of repeatable, code-driven setup a GTM Engineer would own.

The Salesforce version of this build lives at [mindofhenry/doom-inc-sfdc](https://github.com/mindofhenry/doom-inc-sfdc).

---

## Why I Built This

The companion to DOOM Inc SFDC. Salesforce and HubSpot have fundamentally different object models — Salesforce centers on Leads that convert to Contacts/Accounts, while HubSpot treats Contacts, Companies, and Deals as separate first-class objects with associations. This build reflects those differences rather than papering over them.

The Python API approach was chosen over UI configuration deliberately: scripts are repeatable, version-controlled, and deployable against any HubSpot portal. That's how a GTM Engineer would actually stand up a new org.

---

## What's Built

### Custom Contact Properties (7)

Created via `scripts/create_properties.py` using the HubSpot CRM Properties API:

| Property | Internal Name | Type | Purpose |
|---|---|---|---|
| GTM Segment | `gtm_segment` | Dropdown | Enterprise / Mid-Market / Strategic |
| GTM Persona | `gtm_persona` | Dropdown | CISO, VP of Security, IT Director, Security Engineer, Other |
| ICP Fit | `icp_fit` | Dropdown | Strong / Moderate / Weak / Unqualified |
| SLA Tier | `sla_tier` | Dropdown | Tier 1 (1hr) / Tier 2 (4hr) / Tier 3 (24hr) |
| Lead Score | `lead_score` | Number | 0–100 composite score |
| Outbound Sequence | `outbound_sequence` | Text | Active sequence identifier |
| Last Touched By | `last_touched_by` | Dropdown | SDR / AE / Marketing / Partner |

### Seed Contacts (20)

Created via `scripts/seed_contacts.py`. Covers all GTM segments, personas, SLA tiers, and ICP fit ratings.

Segment breakdown:
- Enterprise: 6 contacts (CISO, VP of Security, IT Director, Security Engineer)
- Mid-Market: 6 contacts
- Strategic: 4 contacts
- Mixed high-urgency: 2 contacts
- Catch-all / unqualified: 2 contacts

### Companies (20)

Created via `scripts/create_companies.py`. One Company record per account, with domain, industry, headcount, ARR, city, and state — giving contacts a proper parent object rather than a flat text field.

### Deals (20)

Created via `scripts/create_deals.py`. One Deal per account, distributed across all 7 default pipeline stages (Prospecting → Closed Won/Lost). ACV ranges from $5K (unqualified) to $780K (Strategic), with 2 closed deals for pipeline history.


### Workflow Specs (3)

Documented in `workflows/` as deployment-ready JSON. Built and tested against the HubSpot Automation API — blocked from deploying by HubSpot's subscription tier (Workflows require Sales Hub Professional+). On a paid portal, these would deploy via `scripts/create_workflows.py`.

| Workflow | Trigger | Action |
|---|---|---|
| SLA Tier 1 Breach Alert | SLA Tier = Tier 1 | Creates high-priority task due tomorrow |
| Post-Conversion Follow-Up | Lifecycle Stage = Customer | Creates discovery call task due in 3 days |
| Enterprise Exec Routing | Segment = Enterprise + Persona = CISO or VP | Sets Last Touched By = AE |

**Note on owner assignment:** Direct contact owner rotation via workflow requires Operations Hub. The routing workflow uses a property flag (`last_touched_by`) as a free-tier-compatible proxy for the same logic.

---

## HubSpot Free Tier Limitations

This build documents what's available on HubSpot Free vs. what requires a paid tier:

| Feature | Free | Starter | Professional |
|---|---|---|---|
| Custom properties | ✅ | ✅ | ✅ |
| Contacts / Companies / Deals | ✅ | ✅ | ✅ |
| Active lists | ❌ | ✅ | ✅ |
| Workflows (UI + API) | ❌ | ❌ | ✅ |
| Reports + Dashboards | ❌ | ✅ | ✅ |
| Owner assignment via workflow | ❌ | ❌ | Ops Hub |

Workflow specs are documented as JSON in `workflows/` to demonstrate the design regardless of deployment constraints.

---

## Repo Structure

```
doom-inc-hubspot/
├── scripts/
│   ├── create_properties.py    # 7 custom contact properties
│   ├── seed_contacts.py        # 20 mock contacts
│   ├── create_companies.py     # 20 company records
│   ├── create_deals.py         # 20 deals across pipeline stages
│   └── create_workflows.py     # workflow API (blocked on free tier)
├── workflows/
│   ├── sla_tier1_breach.json           # SLA breach alert spec
│   ├── post_conversion_followup.json   # post-conversion task spec
│   └── enterprise_exec_routing.json    # routing logic spec
├── .env                        # HUBSPOT_ACCESS_TOKEN (gitignored)
├── .gitignore
└── README.md
```

---

## How to Deploy

Prerequisites: Python 3, a HubSpot account (free tier works for properties/contacts/companies/deals), a Private App token.

```bash
# Clone and install
git clone https://github.com/mindofhenry/doom-inc-hubspot
cd doom-inc-hubspot
pip install hubspot-api-client python-dotenv requests

# Add your token
echo "HUBSPOT_ACCESS_TOKEN=your-token-here" > .env

# Run in order
python scripts/create_properties.py
python scripts/seed_contacts.py
python scripts/create_companies.py
python scripts/create_deals.py
```

Private App requires these scopes:
- `crm.objects.contacts.read` / `crm.objects.contacts.write`
- `crm.schemas.contacts.read` / `crm.schemas.contacts.write`
- `crm.objects.companies.read` / `crm.objects.companies.write`
- `crm.objects.deals.read` / `crm.objects.deals.write`
- `crm.objects.owners.read`

---

## Stack

- **HubSpot CRM** (Free tier)
- **Python 3** + `hubspot-api-client` v12 + `requests` + `python-dotenv`
- **HubSpot CRM API** (Properties, Contacts, Companies, Deals)
- **HubSpot Automation API v3** (workflow specs — requires Professional+)
- **Git / GitHub**

---

*Built by [Henry Marble](https://linkedin.com/in/henry-marble) as part of a portfolio targeting GTM Engineering / Revenue Operations roles.*
