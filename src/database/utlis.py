import uuid

def generate_uuids(count):
    """
    Generate a list of UUIDs based on the given count.

    Args:
        count (int): The number of UUIDs to generate.

    Returns:
        list: A list containing the generated UUIDs.
    """
    uuid_list = [str(uuid.uuid4()) for _ in range(count)]
    return uuid_list