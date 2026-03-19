from pydantic import BaseModel

class DataModel(BaseModel):
    """
    Wallet address

    This field represents the wallet address of the user who owns the data.
    """
    wallet_address: dict

class EventModel(BaseModel):
    """
    Event

    This field represents the event data.
    """
    event_data: dict