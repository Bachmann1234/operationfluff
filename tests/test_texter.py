import datetime
from unittest.mock import call

from operation_fluff.dog_finder import Dog
from operation_fluff.texter import format_dog_for_mms, text_dogs


def test_format_dog() -> None:
    assert format_dog_for_mms(
        Dog(
            breed="West Highland White Terrier / Westie Mix",
            age="Adult",
            name="Leo",
            photo="https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/49150408/6/?bust=1600538556",
            profile_url="https://www.petfinder.com/dog/leo-49150408/ma/andover/great-dog-rescue-new-england-ma224/",
            published_at=datetime.datetime(
                2020, 9, 19, 18, 2, 43, tzinfo=datetime.timezone.utc
            ),
        )
    ) == (
        "Leo is an adult West Highland White Terrier / Westie Mix\nhttps://www.petfinder.com/dog/leo-49150408/ma/andover/great-dog-rescue-new-england-ma224/",
        "https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/49150408/6/?bust=1600538556",
    )

    assert format_dog_for_mms(
        Dog(
            breed="Bernese Mountain Dog",
            age="Young",
            name="Mr. Charlie",
            photo="https://example.com/photo",
            profile_url="https://example.com/profile",
            published_at=datetime.datetime(
                2020, 9, 19, 18, 2, 43, tzinfo=datetime.timezone.utc
            ),
        )
    ) == (
        "Mr. Charlie is a young Bernese Mountain Dog\nhttps://example.com/profile",
        "https://example.com/photo",
    )


def test_text_dogs(mocker) -> None:
    dogs = [
        Dog(
            breed="Bernese Mountain Dog",
            age="Young",
            name="Mr. Charlie",
            photo="https://example.com/photo",
            profile_url="https://example.com/profile",
            published_at=datetime.datetime(
                2020, 9, 19, 18, 2, 43, tzinfo=datetime.timezone.utc
            ),
        ),
        Dog(
            breed="Newfoundland",
            age="Young",
            name="Jupiter",
            photo="https://example.com/photo",
            profile_url="https://example.com/profile",
            published_at=datetime.datetime(
                2020, 9, 19, 18, 2, 43, tzinfo=datetime.timezone.utc
            ),
        ),
    ]
    client_mock = mocker.patch("operation_fluff.texter.Client")
    message_ids = text_dogs(
        dogs, ["2025550135", "2025550117"], "2025550135", "sid", "auth"
    )
    assert len(message_ids) == 4
    assert client_mock.mock_calls == [
        call("sid", "auth"),
        call().messages.create(
            body="Mr. Charlie is a young Bernese Mountain Dog\nhttps://example.com/profile",
            from_="2025550135",
            media_url="https://example.com/photo",
            to="2025550135",
        ),
        call().messages.create(
            body="Mr. Charlie is a young Bernese Mountain Dog\nhttps://example.com/profile",
            from_="2025550135",
            media_url="https://example.com/photo",
            to="2025550117",
        ),
        call().messages.create(
            body="Jupiter is a young Newfoundland\nhttps://example.com/profile",
            from_="2025550135",
            media_url="https://example.com/photo",
            to="2025550135",
        ),
        call().messages.create(
            body="Jupiter is a young Newfoundland\nhttps://example.com/profile",
            from_="2025550135",
            media_url="https://example.com/photo",
            to="2025550117",
        ),
    ]
