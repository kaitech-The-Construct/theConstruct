# api/routers/blockchain.py

from core.services.blockchain_service import BlockchainService
from core.services.cross_chain_service import CrossChainService
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
blockchain_service = BlockchainService()
cross_chain_service = CrossChainService()


@router.post("/xrpl/tokenize")
async def tokenize_asset(asset_data: dict):
    """
    Create an asset token on the XRPL.
    """
    result = blockchain_service.create_asset_token(asset_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Tokenization failed"),
        )
    return result


@router.post("/xrpl/trade")
async def execute_trade(trade_order: dict):
    """
    Execute a trade on the XRPL DEX.
    """
    result = blockchain_service.execute_dex_trade(trade_order)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "DEX trade failed"),
        )
    return result


@router.post("/xrpl/escrow")
async def create_escrow(escrow_params: dict):
    """
    Create an escrow on the XRPL.
    """
    result = blockchain_service.create_escrow(escrow_params)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Escrow creation failed"),
        )
    return result


@router.post("/solana/deploy")
async def deploy_contract(contract_data: dict):
    """
    Deploy a smart contract on Solana.
    """
    contract_code = contract_data.get("code")
    if not contract_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contract code is required",
        )
    result = blockchain_service.deploy_smart_contract(contract_code)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Deployment failed"),
        )
    return result


@router.post("/solana/execute")
async def execute_contract(execution_data: dict):
    """
    Execute a function on a Solana smart contract.
    """
    contract_id = execution_data.get("contract_id")
    function = execution_data.get("function")
    params = execution_data.get("params")
    if not all([contract_id, function, params]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contract ID, function, and params are required",
        )
    result = blockchain_service.execute_contract_function(
        contract_id, function, params
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Execution failed"),
        )
    return result


@router.post("/crosschain/bridge")
async def bridge_assets(bridge_data: dict):
    """
    Bridge assets between supported chains.
    """
    source_chain = bridge_data.get("source_chain")
    target_chain = bridge_data.get("target_chain")
    asset_data = bridge_data.get("asset_data")
    if not all([source_chain, target_chain, asset_data]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source chain, target chain, and asset data are required",
        )
    result = cross_chain_service.bridge_assets(source_chain, target_chain, asset_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Asset bridging failed"),
        )
    return result


@router.get("/crosschain/portfolio/{user_address}")
async def get_portfolio(user_address: str):
    """
    Aggregate user portfolio across all supported chains.
    """
    result = cross_chain_service.aggregate_portfolio(user_address)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Portfolio aggregation failed"),
        )
    return result


@router.get("/crosschain/history/{user_id}")
async def get_transaction_history(user_id: str):
    """
    Get transaction history for a user across all supported chains.
    """
    history = cross_chain_service.sync_transaction_history(user_id)
    return {"history": history}


@router.get("/xrpl/balance/{address}")
async def get_xrpl_balance(address: str):
    """
    Get wallet balance on XRPL.
    """
    transactions = blockchain_service.monitor_transactions(address)
    return {"address": address, "transactions": transactions, "chain": "xrpl"}


@router.post("/xrpl/validate")
async def validate_xrpl_payment(validation_data: dict):
    """
    Validate a payment transaction on XRPL.
    """
    transaction_hash = validation_data.get("transaction_hash")
    if not transaction_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction hash is required",
        )
    
    result = blockchain_service.validate_payment(transaction_hash)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Payment validation failed"),
        )
    return result


@router.get("/solana/reputation/{address}")
async def get_solana_reputation(address: str):
    """
    Get reputation score for a user on Solana.
    """
    result = blockchain_service.track_reputation_score(address)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Reputation tracking failed"),
        )
    return result


@router.post("/solana/vote")
async def cast_governance_vote(vote_data: dict):
    """
    Cast a governance vote on Solana.
    """
    proposal_id = vote_data.get("proposal_id")
    if not proposal_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Proposal ID is required",
        )
    
    result = blockchain_service.manage_governance_voting(proposal_id, vote_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Governance voting failed"),
        )
    return result


@router.post("/solana/subscription")
async def process_subscription_payment(subscription_data: dict):
    """
    Process subscription payment on Solana.
    """
    result = blockchain_service.handle_subscription_payments(subscription_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Subscription payment failed"),
        )
    return result


@router.post("/crosschain/validate")
async def validate_cross_chain_transaction(validation_data: dict):
    """
    Validate a cross-chain transaction.
    """
    result = cross_chain_service.validate_cross_chain_transaction(validation_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Cross-chain validation failed"),
        )
    return result
