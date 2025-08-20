from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class OrderType(str, Enum):
    BUY = "buy"
    SELL = "sell"

class AssetType(str, Enum):
    COMPONENT = "component"
    MATERIAL = "material"
    TOOL = "tool"
    SERVICE = "service"

class GetAccountInfoRequest(BaseModel):
    address: str = Field(..., description="XRPL account address")

class TokenizeAssetRequest(BaseModel):
    asset_name: str = Field(..., description="Name of the asset to tokenize")
    asset_description: str = Field(..., description="Description of the asset")
    asset_type: AssetType = Field(..., description="Type of asset")
    quantity: int = Field(..., gt=0, description="Quantity of tokens to create")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    specifications: Optional[Dict[str, Any]] = Field(None, description="Technical specifications")
    manufacturer_info: Optional[Dict[str, str]] = Field(None, description="Manufacturer information")

class CreateOrderRequest(BaseModel):
    order_type: OrderType = Field(..., description="Type of order (buy/sell)")
    asset_code: str = Field(..., description="Asset code to trade")
    amount: float = Field(..., gt=0, description="Amount to trade")
    price: float = Field(..., gt=0, description="Price per unit")
    expiration: Optional[datetime] = Field(None, description="Order expiration time")

class CreateEscrowRequest(BaseModel):
    destination: str = Field(..., description="Destination XRPL address")
    amount: float = Field(..., gt=0, description="Amount to escrow")
    condition: Optional[str] = Field(None, description="Escrow condition")
    finish_after: Optional[datetime] = Field(None, description="Earliest time to finish escrow")
    condition_fulfillment: Optional[str] = Field(None, description="Condition fulfillment")

class WalletConnectionRequest(BaseModel):
    wallet_address: str = Field(..., description="Wallet address to connect")
    wallet_type: str = Field(default="xumm", description="Type of wallet")
    public_key: Optional[str] = Field(None, description="Public key")

class ManufacturingOrderRequest(BaseModel):
    component_id: str = Field(..., description="Component ID to manufacture")
    quantity: int = Field(..., gt=0, description="Quantity to manufacture")
    specifications: Dict[str, Any] = Field(..., description="Manufacturing specifications")
    delivery_address: str = Field(..., description="Delivery address")
    max_price: float = Field(..., gt=0, description="Maximum price willing to pay")
    deadline: datetime = Field(..., description="Manufacturing deadline")

class QualityAssuranceRequest(BaseModel):
    order_id: str = Field(..., description="Manufacturing order ID")
    quality_metrics: Dict[str, Any] = Field(..., description="Quality assessment metrics")
    passed: bool = Field(..., description="Whether quality check passed")
    inspector_id: str = Field(..., description="Quality inspector ID")
    notes: Optional[str] = Field(None, description="Additional notes")

# Response schemas
class StandardResponseData(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    timestamp: str
    service: str
    error_code: Optional[str] = None
    details: Optional[Any] = None

class TokenizationResponse(BaseModel):
    transaction_hash: str
    asset_id: str
    token_count: int
    issuer_address: str
    created_at: datetime

class OrderResponse(BaseModel):
    order_id: str
    transaction_hash: str
    status: str
    created_at: datetime

class EscrowResponse(BaseModel):
    escrow_id: str
    transaction_hash: str
    status: str
    amount: float
    destination: str
    created_at: datetime

class AccountInfoResponse(BaseModel):
    address: str
    balance: float
    sequence: int
    account_data: Dict[str, Any]
    trust_lines: Optional[list] = None

class NetworkInfoResponse(BaseModel):
    network_id: str
    ledger_index: int
    ledger_hash: str
    validated: bool
    reserve_base: float
    reserve_inc: float
