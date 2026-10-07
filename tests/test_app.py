import app


def sample_data(conversion_id="abc123"):
    return {
        "conversionId": conversion_id,
        "fields": [
            {"name": "email", "value": "nora.weiss@routewise.io"},
            {"name": "firstname", "value": "Nora"},
            {"name": "lastname", "value": "Weiss"},
            {"name": "jobtitle", "value": "Head of Sales"},
        ],
    }


def test_parse_form():
    lead = app.parse_form(sample_data())
    assert lead["email"] == "nora.weiss@routewise.io"
    assert lead["name"] == "Nora Weiss"
    assert lead["domain"] == "routewise.io"


def test_duplicate_lead_is_skipped(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # so the test files don't end up in the repo
    monkeypatch.setattr("config.SLACK_BOT_TOKEN", None)
    monkeypatch.setattr("config.ANTHROPIC_API_KEY", None)

    first = app.handle_lead(sample_data())
    second = app.handle_lead(sample_data())

    assert first["status"] == "done"
    assert first["rep"] == "Jalal Abdelrahim"
    assert second["status"] == "duplicate"


def test_missing_email_is_skipped():
    data = {"fields": [{"name": "firstname", "value": "Bob"}]}
    assert app.handle_lead(data)["status"] == "skipped"
