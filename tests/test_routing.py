from routing import pick_rep


def test_big_company_goes_to_enterprise():
    assert pick_rep({"employees": 5000}, 80)["name"] == "Avery Chen"


def test_mid_company_goes_to_mid_market():
    assert pick_rep({"employees": 500}, 80)["name"] == "Riley Nguyen"


def test_small_company_goes_to_smb():
    assert pick_rep({"employees": 40}, 80)["name"] == "Jalal Abdelrahim"


def test_low_score_gets_no_rep():
    assert pick_rep({"employees": 5000}, 20) is None
