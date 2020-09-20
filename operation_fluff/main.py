import os

from operation_fluff.emailer import email_dogs
from operation_fluff.query import find_new_dogs

if __name__ == "__main__":
    dogs = list(find_new_dogs(since_mins=int(os.environ.get("TIME_BETWEEN_RUNS"))))
    print(f"I found {len(dogs)} new dogs!")
    result = email_dogs(dogs)
    print(f"email request status: {result.status_code}")
