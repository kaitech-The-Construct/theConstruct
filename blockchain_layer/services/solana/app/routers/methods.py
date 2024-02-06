import json
from core.services.methods import (
    SolanaService,
)
from fastapi import HTTPException, APIRouter
from schemas.schema import GetMultipleAccountsRequest, SendTransactionRequest
from utils.common import get_pubkey, get_pubkeys

router = APIRouter()
solana_service = SolanaService()



@router.get("/get_account_info/{address}")
async def get_account_info(address: str):
    try:
        print(f'Address: {address}')
        pub_key = get_pubkey(address)
        print(f'PubKey: {pub_key}')
        data = solana_service.get_account_info(pub_key)
        response = str(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@router.get("/get_balance/{address}")
async def get_balance(address: str):
    try:
        pub_key = get_pubkey(address)
        response = solana_service.get_balance(pub_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@router.post("/get_multiple_accounts")
async def get_multiple_accounts(request: GetMultipleAccountsRequest):
    try:
        pub_keys = get_pubkeys(request.addresses)
        response = solana_service.get_multiple_accounts(pub_keys)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@router.get("/get_program_accounts/{program_pub_key}")
async def get_program_accounts(program_pub_key: str):
    try:
        response = solana_service.get_program_accounts(program_pub_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@router.get("/get_supply")
async def get_supply():
    try:
        response = solana_service.get_supply()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


# ... Add more routes for each method in SolanaService ...


@router.get("/get_token_supply/{token_mint_pub_key}")
async def get_token_supply(token_mint_pub_key: str):
    try:
        response = solana_service.get_token_supply(token_mint_pub_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@router.get("/get_transaction/{tx_signature}")
async def get_transaction(tx_signature: str):
    try:
        response = solana_service.get_transaction(tx_signature)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@router.get("/get_version")
async def get_version():
    try:
        response = solana_service.get_version()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@router.post("/send_transaction")
async def send_transaction(request: SendTransactionRequest):
    try:
        response = solana_service.send_transaction(request.transaction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response
