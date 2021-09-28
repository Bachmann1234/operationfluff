import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Generator, List

import requests
from redis import Redis
from requests import HTTPError
from retry import retry


@dataclass
class Dog:
    breed: str
    age: str
    name: str
    photo: str
    profile_url: str
    published_at: datetime


def format_dog(dog_to_format: Dict) -> Dog:
    photo = dog_to_format.get("primary_photo_cropped_url")
    if not photo:
        # I wanna see if I have an alternative if there is no dog
        print(json.dumps(dog_to_format, indent=4))
        photo = ""
    return Dog(
        breed=dog_to_format["breeds_label"],
        age=dog_to_format["age"],
        name=dog_to_format["name"],
        photo=photo,
        profile_url=dog_to_format["social_sharing"]["email_url"],
        published_at=datetime.strptime(
            dog_to_format["published_at"], "%Y-%m-%dT%H:%M:%S%z"
        ),
    )


@retry(HTTPError, tries=3, delay=1, backoff=2, jitter=1)
def get_dogs(limit: int = 300) -> Generator[Dog, None, None]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) "
        "Gecko/20100101 Firefox/80.0",
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
        response.raise_for_status()
        result = response.json()["result"]
        total_pages = result["pagination"]["total_pages"]
        for animal in result.get("animals", []):
            yield format_dog(animal["animal"])


def find_new_dogs(since_mins: int = 10, redis_cache: Redis = None) -> List[Dog]:
    cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=since_mins)
    new_dogs = []
    seen = set()
    try:
        retrieved_dogs = get_dogs()
    except HTTPError as e:
        print(e)
        if e.response.status_code < 500:
            raise
        retrieved_dogs = []

    for potential_dog in retrieved_dogs:
        if (
            potential_dog.published_at > cutoff_time
            and potential_dog.profile_url not in seen
        ):
            if not redis_cache or redis_cache.get(potential_dog.profile_url) is None:
                new_dogs.append(potential_dog)
                seen.add(potential_dog.profile_url)
                if redis_cache:
                    redis_cache.set(potential_dog.profile_url, ex=86400, value="seen")
    return new_dogs


if __name__ == "__main__":
    from pprint import pprint

    for dog in find_new_dogs(1440):
        pprint(dog)
