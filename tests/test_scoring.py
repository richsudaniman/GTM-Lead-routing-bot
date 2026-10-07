from scoring import score_with_rules, score_lead


def make_lead(email="nora@routewise.io", title="Head of Sales"):
    return {"name": "Test", "email": email, "domain": email.split("@")[1], "title": title, "message": ""}


def test_good_lead_scores_high():
    company = {"name": "Routewise", "industry": "Fintech", "employees": 300, "country": "DE"}
    score, reason = score_with_rules(make_lead(), company)
    assert score == 100


def test_unknown_company_scores_low():
    company = {"name": "?", "industry": "Unknown", "employees": 0, "country": "Unknown"}
    score, reason = score_with_rules(make_lead(title="Intern"), company)
    assert score == 30
    assert reason == "no strong signals"


def test_gmail_gets_zero():
    company = {"name": "?", "industry": "Unknown", "employees": 0, "country": "Unknown"}
    score, reason = score_lead(make_lead(email="someone@gmail.com"), company)
    assert score == 0
