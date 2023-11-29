# core/utils/common.py

import random
import string
from datetime import datetime, timedelta

import bleach


def generate_random_string(length: int = 12) -> str:
    """
    Generate a random string of fixed length.
    """
    letters_and_digits = string.ascii_letters + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(length))


def convert_timedelta_to_seconds(timedelta_obj: timedelta) -> int:
    """
    Convert a timedelta object to total seconds.
    """
    return int(timedelta_obj.total_seconds())


def get_current_utc_time() -> datetime:
    """
    Retrieve the current UTC time.
    """
    return datetime.utcnow()


def calculate_expiry_time(seconds: int) -> datetime:
    """
    Calculate the expiry time from now given a number of seconds.
    """
    return get_current_utc_time() + timedelta(seconds=seconds)


def sanitize_html(raw_html: str) -> str:
    """
    Sanitize raw HTML strings to prevent XSS attacks.
    """
    # Bleach provides a clean function that will escape or strip any tags or attributes that are not explicitly allowed.
    # Adapt the tags and attributes to your application's requirements for allowed content.

    allowed_tags = ["p", "b", "i", "u", "em", "strong", "a"]
    allowed_attributes = {"a": ["href", "title"]}
    cleaned_html = bleach.clean(
        raw_html, tags=allowed_tags, attributes=allowed_attributes
    )
    return cleaned_html


def count_unique_items_by_key(json_list: list, key: str) -> int:
    """Count the number of unique items in a JSON list by key.

    Args:
        json_list: A list of JSON objects.
        key: The key to use for counting unique items.

    Returns:
        The number of unique items in the JSON list by key.
    """

    unique_items = {}

    # Iterate through the JSON list
    for item in json_list:
        if key in item:
            # Extract the value of the specified key
            value = item[key]

            # Check if the value is already in the dictionary
            if value not in unique_items:
                # If not, add it as a key with a count of 1
                unique_items[value] = 1
            else:
                # If it's already in the dictionary, increment the count
                unique_items[value] += 1

    return len(unique_items)
