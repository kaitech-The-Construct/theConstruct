from solana.transaction import Pubkey


def get_pubkey(address: str) -> Pubkey:
    """
    Convert a string representation of the address to a Pubkey object.

    Args:
        address (str): The string wallet address.

    Returns:
        Pubkey: The Pubkey object.
    """
    key = Pubkey.from_string(address)
    return key


def get_pubkeys(address_list):
    """
    Convert a list of addresses to Pubkey objects.

    Args:
        address_list (list[str]): List of string representations of addresses.

    Returns:
        list[Pubkey]: List of Pubkey objects.
    """
    pubkeys = [get_pubkey(address) for address in address_list]
    return pubkeys
