import os
from dataclasses import dataclass
from typing import List

from operation_fluff.emailer import email_dogs, email_error
from operation_fluff.dog_finder import find_new_dogs


@dataclass
class Config:
    time_between_runs: int
    sender: str
    receivers: List[str]
    sendgrid_api_key: str
    admin_email: str


def load_config() -> Config:
    return Config(
        time_between_runs=int(os.environ["TIME_BETWEEN_RUNS"]),
        sender=os.environ["SENDER"],
        receivers=os.environ["RECEIVER"].split(","),
        sendgrid_api_key=os.environ["SENDGRID_API_KEY"],
        admin_email=os.environ["ADMIN_EMAIL"],
    )


def main() -> None:
    config = load_config()
    try:
        dogs = list(find_new_dogs(since_mins=config.time_between_runs))
        print(f"I found {len(dogs)} new dogs!")
        if dogs:
            print("Sending new dogs")
            result = email_dogs(
                dogs, config.sender, config.receivers, config.sendgrid_api_key
            )
            print(f"email request status: {result.status_code}")
    except Exception as e:
        print(f"Failed to query/message dogs ({str(e)})")
        email_error(
            str(e), config.sender, [config.admin_email], config.sendgrid_api_key
        )


if __name__ == "__main__":
    main()
