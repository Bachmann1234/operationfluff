import datetime
from unittest.mock import call

from operation_fluff.dog_finder import Dog
from operation_fluff.emailer import email_dogs, email_error, email_template


def test_email_error(mocker) -> None:
    client_mock = mocker.patch("operation_fluff.emailer.SendGridAPIClient")
    email_error("OMG NO", "from@from.com", ["to@to.com"], "apikey")
    assert len(client_mock.mock_calls) == 2
    assert client_mock.mock_calls[0] == call("apikey")
    email_sent = client_mock.mock_calls[1].args[0]
    assert email_sent.from_email.email == "from@from.com"
    assert email_sent.subject.subject == "Operation Fluff Error"
    assert email_sent.contents[0].content == "OMG NO"
    assert email_sent.contents[0].mime_type == "text/plain"
    assert email_sent.personalizations[0].tos == [{"email": "to@to.com"}]


def test_email_dogs(mocker) -> None:
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
    client_mock = mocker.patch("operation_fluff.emailer.SendGridAPIClient")
    email_dogs(dogs, "from@from.com", ["to@to.com", "alsoTo@to.com"], "apikey")
    assert len(client_mock.mock_calls) == 2
    assert client_mock.mock_calls[0] == call("apikey")
    email_sent = client_mock.mock_calls[1].args[0]
    assert email_sent.from_email.email == "from@from.com"
    assert email_sent.subject.subject == "New Dogs!"
    assert email_sent.contents[0].content == email_template.render(dogs=dogs)
    assert email_sent.contents[0].mime_type == "text/html"
    assert email_sent.personalizations[0].tos == [
        {"email": "to@to.com"},
        {"email": "alsoTo@to.com"},
    ]


def test_template() -> None:
    dogs = [
        Dog(
            breed="West Highland White Terrier / Westie Mix",
            age="Adult",
            name="Leo",
            photo="https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/49150408/6/?bust=1600538556",
            profile_url="https://www.petfinder.com/dog/leo-49150408/ma/andover/great-dog-rescue-new-england-ma224/",
            published_at=datetime.datetime(
                2020, 9, 19, 18, 2, 43, tzinfo=datetime.timezone.utc
            ),
        ),
        Dog(
            breed="Anatolian Shepherd & Border Collie Mix",
            age="Young",
            name="Buddy - local boy",
            photo="https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/49149083/4/?bust=1600530983",
            profile_url="https://www.petfinder.com/dog/buddy-local-boy-49149083/ma/andover/great-dog-rescue-new-england-ma224/",
            published_at=datetime.datetime(
                2020, 9, 19, 15, 56, 29, tzinfo=datetime.timezone.utc
            ),
        ),
    ]

    assert (
        email_template.render(dogs=dogs)
        == """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "https://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="https://www.w3.org/1999/xhtml">
<head>
<title>Test Email Sample</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="viewport" content="width=device-width, initial-scale=1.0 " />
    <style>
        img {
            width: 200px;
        }
    </style>
</head>
<body>

    <div>
        Leo
    </div>
    <div>
        West Highland White Terrier / Westie Mix
    </div>
    <div>
        Adult
    </div>
    
    <div>
        <a href="https://www.petfinder.com/dog/leo-49150408/ma/andover/great-dog-rescue-new-england-ma224/">
            <img src="https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/49150408/6/?bust=1600538556">
        </a>
    </div>
    <hr/>

    <div>
        Buddy - local boy
    </div>
    <div>
        Anatolian Shepherd & Border Collie Mix
    </div>
    <div>
        Young
    </div>
    
    <div>
        <a href="https://www.petfinder.com/dog/buddy-local-boy-49149083/ma/andover/great-dog-rescue-new-england-ma224/">
            <img src="https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/49149083/4/?bust=1600530983">
        </a>
    </div>
    <hr/>

</body>"""
    )
