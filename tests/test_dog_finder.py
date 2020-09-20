import datetime

import pytest
from freezegun import freeze_time

from operation_fluff.dog_finder import get_dogs, Dog, find_new_dogs


@pytest.mark.vcr()
def test_get_dogs() -> None:
    dogs = list(get_dogs(limit=55))
    assert len(dogs) == 105
    assert dogs[0] == Dog(
        breed="Black Labrador Retriever & Golden Retriever Mix",
        age="Baby",
        name="Puppies! Black Lab/retriever mix puppies!",
        photo="https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/48985989/3/?bust=1599273048",
        profile_url="https://www.petfinder.com/dog/puppies-black-lab-retriever-mix-puppies-48985989/ma/cambridge/rocios-rescues-tx2389/",
        published_at=datetime.datetime(
            2020, 9, 5, 2, 56, 40, tzinfo=datetime.timezone.utc
        ),
    )


@pytest.mark.vcr()
@freeze_time("2020-09-20 06:00:00")
def test_get_dogs_since() -> None:
    result = list(find_new_dogs(since_mins=1000))
    assert result == [
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
        Dog(
            breed="Catahoula Leopard Dog Mix",
            age="Baby",
            name="Jannelle",
            photo="https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/49148790/3/?bust=1600528963",
            profile_url="https://www.petfinder.com/dog/jannelle-49148790/ri/warwick/cenla-alliance-for-animals-la366/",
            published_at=datetime.datetime(
                2020, 9, 19, 15, 23, 36, tzinfo=datetime.timezone.utc
            ),
        ),
        Dog(
            breed="Husky Mix",
            age="Adult",
            name="Buddy, a sweet and gentle loving boy!",
            photo="https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/49148156/4/?bust=1600524902",
            profile_url="https://www.petfinder.com/dog/buddy-a-sweet-and-gentle-loving-boy-49148156/ct/east-hartford/freedom-street-rescue-tx1775/",
            published_at=datetime.datetime(
                2020, 9, 19, 14, 31, 13, tzinfo=datetime.timezone.utc
            ),
        ),
        Dog(
            breed="Siberian Husky & Alaskan Malamute Mix",
            age="Young",
            name="~Kita and bourbon~",
            photo="https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/49149725/2/?bust=1600534381",
            profile_url="https://www.petfinder.com/dog/kita-and-bourbon-49149725/ct/west-hartford/great-divide-animal-rescue-inc-nc1007/",
            published_at=datetime.datetime(
                2020, 9, 19, 16, 56, 38, tzinfo=datetime.timezone.utc
            ),
        ),
    ]
