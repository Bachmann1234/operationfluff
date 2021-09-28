from typing import Tuple, List

from twilio.rest import Client

from operation_fluff.dog_finder import Dog


def format_dog_for_mms(dog: Dog) -> Tuple[str, str]:
    article = "an" if dog.age.lower() == "adult" else "a"
    return (
        f"{dog.name} is {article} {dog.age.lower()} {dog.breed}\n{dog.profile_url}",
        dog.photo,
    )


def text_dogs(
    dogs: List[Dog],
    to_numbers: List[str],
    from_number: str,
    account_sid: str,
    auth_token: str,
):
    client = Client(account_sid, auth_token)
    sent_message_ids = []
    for dog in dogs:
        body, photo_url = format_dog_for_mms(dog)
        for number in to_numbers:
            message = client.messages.create(
                body=body,
                from_=from_number,
                media_url=[photo_url],
                to=number,
            )
            sent_message_ids.append(message.sid)
    return sent_message_ids
