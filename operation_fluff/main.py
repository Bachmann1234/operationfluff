import os
from dataclasses import dataclass
from typing import List

from operation_fluff.emailer import email_dogs, email_error
from operation_fluff.dog_finder import find_new_dogs, Dog
from operation_fluff.texter import text_dogs


@dataclass
class Config:
    time_between_runs: int
    sender: str
    email_subscribers: List[str]
    text_subscribers: List[str]
    sendgrid_api_key: str
    admin_email: str
    twilio_sid: str
    twilio_auth: str
    twilio_phone: str


def load_config() -> Config:
    return Config(
        time_between_runs=int(os.environ["TIME_BETWEEN_RUNS"]),
        sender=os.environ["SENDER"],
        email_subscribers=os.environ["EMAIL_SUBSCRIBERS"].split(","),
        text_subscribers=os.environ["TEXT_SUBSCRIBERS"].split(","),
        sendgrid_api_key=os.environ["SENDGRID_API_KEY"],
        admin_email=os.environ["ADMIN_EMAIL"],
        twilio_sid=os.environ["TWILIO_SID"],
        twilio_auth=os.environ["TWILIO_AUTH"],
        twilio_phone=os.environ["TWILIO_PHONE"],
    )


def send_dogs(dogs: List[Dog], config: Config) -> None:
    if config.email_subscribers:
        email_result = email_dogs(
            dogs, config.sender, config.email_subscribers, config.sendgrid_api_key
        )
        print(f"email request status: {email_result.status_code}")
    if config.text_subscribers:
        text_results = text_dogs(
            dogs,
            config.text_subscribers,
            config.twilio_phone,
            config.twilio_sid,
            config.twilio_auth,
        )
        print(f"Messages sent {','.join(text_results)}")


def main() -> None:
    config = load_config()
    try:
        dogs = list(find_new_dogs(since_mins=config.time_between_runs))
        print(f"I found {len(dogs)} new dogs!")
        if dogs:
            print("Sending new dogs")
            send_dogs(dogs, config)
    except Exception as e:
        print(f"Failed to query/message dogs ({str(e)})")
        email_error(
            str(e), config.sender, [config.admin_email], config.sendgrid_api_key
        )


if __name__ == "__main__":
    main()
