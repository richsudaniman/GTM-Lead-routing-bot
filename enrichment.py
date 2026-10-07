# TODO: hook this up to a real enrichment API (clearbit / apollo)
# using fake data for now so the rest of the app can be tested

FAKE_COMPANIES = {
    "routewise.io": {"name": "Routewise", "industry": "Fintech", "employees": 45, "country": "DE"},
    "northwind-logistics.com": {"name": "Northwind Logistics", "industry": "Logistics", "employees": 850, "country": "US"},
    "megacorp.com": {"name": "MegaCorp", "industry": "SaaS", "employees": 9000, "country": "US"},
    "pixelcraft.design": {"name": "Pixelcraft", "industry": "Agency", "employees": 12, "country": "CA"},
}


def get_company(domain):
    company = FAKE_COMPANIES.get(domain)
    if company is None:
        # we don't know this company
        return {"name": domain, "industry": "Unknown", "employees": 0, "country": "Unknown"}
    return company
