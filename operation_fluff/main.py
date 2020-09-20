import os
from dataclasses import dataclass
from typing import List

from operation_fluff.emailer import email_dogs
from operation_fluff.dog_finder import find_new_dogs


@dataclass
class Config:
    time_between_runs: int
    sender: str
    receivers: List[str]
    sendgrid_api_key: str


def load_config() -> Config:
    return Config(
        time_between_runs=int(os.environ["TIME_BETWEEN_RUNS"]),
        sender=os.environ["SENDER"],
        receivers=os.environ["RECEIVER"].split(","),
        sendgrid_api_key=os.environ["SENDGRID_API_KEY"],
    )


def main() -> None:
    config = load_config()
    dogs = list(find_new_dogs(since_mins=config.time_between_runs))
    print(f"I found {len(dogs)} new dogs!")
    if dogs:
        print("Sending new dogs")
        result = email_dogs(
            dogs, config.sender, config.receivers, config.sendgrid_api_key
        )
        print(f"email request status: {result.status_code}")


if __name__ == "__main__":
    main()
