"""Functions"""

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
