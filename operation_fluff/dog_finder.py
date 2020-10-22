from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict, Generator

import requests


@dataclass
class Dog:
    breed: str
    age: str
    name: str
    photo: str
    profile_url: str
    published_at: datetime


def format_dog(dog: Dict) -> Dog:
    return Dog(
        breed=dog["breeds_label"],
        age=dog["age"],
        name=dog["name"],
        photo=dog["primary_photo_cropped_url"],
        profile_url=dog["social_sharing"]["email_url"],
        published_at=datetime.strptime(dog["published_at"], "%Y-%m-%dT%H:%M:%S%z"),
    )


def get_dogs(limit: int = 300) -> Generator[Dog, None, None]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
    }
    page = 0
    total_pages = 1

    while page != total_pages:
        page += 1
        params = {
            "page": str(page),
            "limit[]": str(limit),
            "status": "adoptable",
            "distance[]": "150",
            "type[]": "dogs",
            "sort[]": "nearest",
            "age[]": ["Adult", "Baby", "Young"],
            "coat_length[]": ["Long", "Medium"],
            "location_slug[]": "us/ma/02144",
            "include_transportable": "true",
        }

        response = requests.get(
            "https://www.petfinder.com/search/", headers=headers, params=params
        )
        result = response.json()["result"]
        total_pages = result["pagination"]["total_pages"]
        for animal in result.get("animals", []):
            yield format_dog(animal["animal"])


def find_new_dogs(since_mins: int = 10) -> Generator[Dog, None, None]:
    cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=since_mins)
    for dog in get_dogs():
        if dog.published_at > cutoff_time:
            yield dog

if __name__ == "__main__":
    from pprint import pprint
    for dog in find_new_dogs(1440):
        pprint(dog)