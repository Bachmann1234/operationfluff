import datetime
from unittest.mock import call

import fakeredis
import pytest

from operation_fluff.dog_finder import Dog
from operation_fluff.main import Config, load_config, main

ADMIN_EMAIL = "person@person.com"
TIME_BETWEEN_RUNS = "10"
SENDER = "rad@rad.com"
EMAIL_SUBSCRIBERS = "cool@cool.com,dude@dude.com"
TEXT_SUBSCRIBERS = "2025550135,2025550117"
SENDGRID_API_KEY = "key"
TWILIO_SID = "sid"
TWILIO_AUTH = "auth"
TWILIO_PHONE = "2025550111"


@pytest.fixture
def example_config(monkeypatch) -> None:
    monkeypatch.setenv("TIME_BETWEEN_RUNS", TIME_BETWEEN_RUNS)
    monkeypatch.setenv("SENDER", SENDER)
    monkeypatch.setenv("EMAIL_SUBSCRIBERS", EMAIL_SUBSCRIBERS)
    monkeypatch.setenv("TEXT_SUBSCRIBERS", TEXT_SUBSCRIBERS)
    monkeypatch.setenv("SENDGRID_API_KEY", SENDGRID_API_KEY)
    monkeypatch.setenv("ADMIN_EMAIL", ADMIN_EMAIL)
    monkeypatch.setenv("TWILIO_SID", TWILIO_SID)
    monkeypatch.setenv("TWILIO_AUTH", TWILIO_AUTH)
    monkeypatch.setenv("TWILIO_PHONE", TWILIO_PHONE)


def test_load_config(example_config) -> None:
    # I repeat here rather than using my constants because
    # I wanna inspect the parsing with my eye
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


def test_send_dogs_success(example_config, mocker):
    redis = fakeredis.FakeStrictRedis()
    example_dog = Dog(
        breed="Bernese Mountain Dog",
        age="Young",
        name="Mr. Charlie",
        photo="https://example.com/photo",
        profile_url="https://example.com/profile",
        published_at=datetime.datetime(
            2020, 9, 19, 18, 2, 43, tzinfo=datetime.timezone.utc
        ),
    )
    email_dogs_mock = mocker.patch("operation_fluff.main.email_dogs")
    email_error_mock = mocker.patch("operation_fluff.main.email_error")
    text_mock = mocker.patch("operation_fluff.main.text_dogs")
    find_new_dogs_mock = mocker.patch(
        "operation_fluff.main.find_new_dogs",
        return_value=[example_dog],
    )
    main(redis)
    assert len(email_dogs_mock.mock_calls) == 2
    assert email_dogs_mock.mock_calls[0] == call(
        [example_dog],
        SENDER,
        EMAIL_SUBSCRIBERS.split(","),
        SENDGRID_API_KEY,
    )
    # The second call is to get the status code of the result but
    # im struggling to capture that in the test and I barely care

    assert email_error_mock.mock_calls == []
    assert text_mock.mock_calls == [
        call(
            [example_dog],
            TEXT_SUBSCRIBERS.split(","),
            TWILIO_PHONE,
            TWILIO_SID,
            TWILIO_AUTH,
        ),
        call().__iter__(),
    ]
    assert find_new_dogs_mock.mock_calls == [
        call(since_mins=int(TIME_BETWEEN_RUNS), redis_cache=redis)
    ]


def test_send_dogs_no_dogs(example_config, mocker):
    redis = fakeredis.FakeStrictRedis()
    email_dogs_mock = mocker.patch("operation_fluff.main.email_dogs")
    email_error_mock = mocker.patch("operation_fluff.main.email_error")
    text_mock = mocker.patch("operation_fluff.main.text_dogs")
    find_new_dogs_mock = mocker.patch(
        "operation_fluff.main.find_new_dogs",
        return_value=[],
    )
    main(redis)
    assert len(email_dogs_mock.mock_calls) == 0
    assert email_error_mock.mock_calls == []
    assert text_mock.mock_calls == []
    assert find_new_dogs_mock.mock_calls == [
        call(since_mins=int(TIME_BETWEEN_RUNS), redis_cache=redis)
    ]


def test_send_dogs_fail(example_config, mocker):
    redis = fakeredis.FakeStrictRedis()
    error_message = "OMG ERROR"
    email_dogs_mock = mocker.patch("operation_fluff.main.email_dogs")
    email_error_mock = mocker.patch("operation_fluff.main.email_error")
    text_mock = mocker.patch("operation_fluff.main.text_dogs")
    find_new_dogs_mock = mocker.patch(
        "operation_fluff.main.find_new_dogs",
        side_effect=ValueError(error_message),
    )
    main(redis)
    assert len(email_dogs_mock.mock_calls) == 0
    assert email_error_mock.mock_calls == [
        call(error_message, SENDER, ADMIN_EMAIL.split(","), SENDGRID_API_KEY),
    ]
    assert text_mock.mock_calls == []
    assert find_new_dogs_mock.mock_calls == [
        call(since_mins=int(TIME_BETWEEN_RUNS), redis_cache=redis)
    ]
