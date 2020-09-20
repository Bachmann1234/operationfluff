from operation_fluff.main import load_config, Config


def test_load_config(monkeypatch) -> None:
    monkeypatch.setenv("TIME_BETWEEN_RUNS", "10")
    monkeypatch.setenv("SENDER", "rad@rad.com")
    monkeypatch.setenv("RECEIVER", "cool@cool.com,dude@dude.com")
    monkeypatch.setenv("SENDGRID_API_KEY", "key")
    monkeypatch.setenv("ADMIN_EMAIL", "person@person.com")

    assert load_config() == Config(
        time_between_runs=10,
        sender="rad@rad.com",
        receivers=["cool@cool.com", "dude@dude.com"],
        sendgrid_api_key="key",
        admin_email="person@person.com",
    )
