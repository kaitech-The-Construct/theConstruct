from pydantic import BaseModel


class GetMultipleAccountsRequest(BaseModel):
    addresses: list[str]


class SendTransactionRequest(BaseModel):
    transaction: str
