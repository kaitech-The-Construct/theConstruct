import json
from datetime import datetime
from typing import Dict, Any
from core.services.methods import XRPLService
from fastapi import HTTPException, APIRouter
from schemas.schema import (
    TokenizeAssetRequest, 
    CreateOrderRequest, 
    CreateEscrowRequest,
    GetAccountInfoRequest
)

router = APIRouter()
xrpl_service = XRPLService()

# Standardized response format (shared with main.py)
class StandardResponse:
    @staticmethod
    def success(data: Any = None, message: str = "Success") -> Dict[str, Any]:
        return {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "service": "xrpl_service"
        }
    
    @staticmethod
    def error(message: str, error_code: str = "GENERAL_ERROR", details: Any = None) -> Dict[str, Any]:
        return {
            "success": False,
            "message": message,
            "error_code": error_code,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
            "service": "xrpl_service"
        }

@router.get("/account/{address}")
async def get_account_info(address: str):
    """Get XRPL account information"""
    try:
        print(f'Getting account info for address: {address}')
        data = await xrpl_service.get_account_info(address)
        return StandardResponse.success(
            data=data,
            message=f"Account information retrieved for {address}"
        )
    except Exception as e:
        print(f"Error getting account info: {str(e)}")
        return StandardResponse.error(
            message="Failed to retrieve account information",
            error_code="ACCOUNT_INFO_ERROR",
            details=str(e)
        )

@router.get("/balance/{address}")
async def get_balance(address: str):
    """Get XRPL account balance"""
    try:
        balance = await xrpl_service.get_balance(address)
        return StandardResponse.success(
            data={"address": address, "balance": balance},
            message="Balance retrieved successfully"
        )
    except Exception as e:
        return StandardResponse.error(
            message="Failed to retrieve balance",
            error_code="BALANCE_ERROR",
            details=str(e)
        )

@router.post("/tokenize")
async def tokenize_asset(request: TokenizeAssetRequest):
    """Tokenize a robotics component as an XRPL asset"""
    try:
        result = await xrpl_service.tokenize_asset(
            asset_name=request.asset_name,
            asset_description=request.asset_description,
            quantity=request.quantity,
            metadata=request.metadata
        )
        return StandardResponse.success(
            data=result,
            message="Asset tokenized successfully"
        )
    except Exception as e:
        return StandardResponse.error(
            message="Failed to tokenize asset",
            error_code="TOKENIZATION_ERROR",
            details=str(e)
        )

@router.post("/orders")
async def create_order(request: CreateOrderRequest):
    """Create a buy/sell order on XRPL DEX"""
    try:
        result = await xrpl_service.create_order(
            order_type=request.order_type,
            asset_code=request.asset_code,
            amount=request.amount,
            price=request.price
        )
        return StandardResponse.success(
            data=result,
            message="Order created successfully"
        )
    except Exception as e:
        return StandardResponse.error(
            message="Failed to create order",
            error_code="ORDER_CREATION_ERROR",
            details=str(e)
        )

@router.get("/orders/{account_address}")
async def get_orders(account_address: str):
    """Get orders for a specific account"""
    try:
        orders = await xrpl_service.get_orders(account_address)
        return StandardResponse.success(
            data=orders,
            message="Orders retrieved successfully"
        )
    except Exception as e:
        return StandardResponse.error(
            message="Failed to retrieve orders",
            error_code="ORDER_RETRIEVAL_ERROR",
            details=str(e)
        )

@router.post("/escrow")
async def create_escrow(request: CreateEscrowRequest):
    """Create an escrow for secure transactions"""
    try:
        result = await xrpl_service.create_escrow(
            destination=request.destination,
            amount=request.amount,
            condition=request.condition,
            finish_after=request.finish_after
        )
        return StandardResponse.success(
            data=result,
            message="Escrow created successfully"
        )
    except Exception as e:
        return StandardResponse.error(
            message="Failed to create escrow",
            error_code="ESCROW_CREATION_ERROR",
            details=str(e)
        )

@router.get("/escrow/{escrow_id}")
async def get_escrow(escrow_id: str):
    """Get escrow information"""
    try:
        escrow_info = await xrpl_service.get_escrow(escrow_id)
        return StandardResponse.success(
            data=escrow_info,
            message="Escrow information retrieved successfully"
        )
    except Exception as e:
        return StandardResponse.error(
            message="Failed to retrieve escrow information",
            error_code="ESCROW_RETRIEVAL_ERROR",
            details=str(e)
        )

@router.get("/orderbook/{asset_code}")
async def get_orderbook(asset_code: str):
    """Get orderbook for a specific asset"""
    try:
        orderbook = await xrpl_service.get_orderbook(asset_code)
        return StandardResponse.success(
            data=orderbook,
            message="Orderbook retrieved successfully"
        )
    except Exception as e:
        return StandardResponse.error(
            message="Failed to retrieve orderbook",
            error_code="ORDERBOOK_ERROR",
            details=str(e)
        )

@router.get("/transaction/{tx_hash}")
async def get_transaction(tx_hash: str):
    """Get transaction details"""
    try:
        transaction = await xrpl_service.get_transaction(tx_hash)
        return StandardResponse.success(
            data=transaction,
            message="Transaction retrieved successfully"
        )
    except Exception as e:
        return StandardResponse.error(
            message="Failed to retrieve transaction",
            error_code="TRANSACTION_ERROR",
            details=str(e)
        )

@router.get("/network/info")
async def get_network_info():
    """Get XRPL network information"""
    try:
        network_info = await xrpl_service.get_network_info()
        return StandardResponse.success(
            data=network_info,
            message="Network information retrieved successfully"
        )
    except Exception as e:
        return StandardResponse.error(
            message="Failed to retrieve network information",
            error_code="NETWORK_INFO_ERROR",
            details=str(e)
        )
