from operation_fluff.main import load_config, Config


def test_load_config(monkeypatch) -> None:
    monkeypatch.setenv("TIME_BETWEEN_RUNS", "10")
    monkeypatch.setenv("SENDER", "rad@rad.com")
    monkeypatch.setenv("EMAIL_SUBSCRIBERS", "cool@cool.com,dude@dude.com")
    monkeypatch.setenv("TEXT_SUBSCRIBERS", "2025550135,2025550117")
    monkeypatch.setenv("SENDGRID_API_KEY", "key")
    monkeypatch.setenv("ADMIN_EMAIL", "person@person.com")
    monkeypatch.setenv("TWILIO_SID", "sid")
    monkeypatch.setenv("TWILIO_AUTH", "auth")
    monkeypatch.setenv("TWILIO_PHONE", "2025550111")

    assert load_config() == Config(
        time_between_runs=10,
        sender="rad@rad.com",
        email_subscribers=["cool@cool.com", "dude@dude.com"],
        text_subscribers=["2025550135", "2025550117"],
        sendgrid_api_key="key",
        admin_email="person@person.com",
        twilio_sid="sid",
        twilio_auth="auth",
        twilio_phone="2025550111",
    )
