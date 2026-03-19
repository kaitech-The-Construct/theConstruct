"""
The Construct Blockchain Layer Data Storage Service
"""
import os
import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from database import db_manager
from repositories import (
    UserRepository, AssetRepository, TradingRepository,
    ManufacturingRepository, GovernanceRepository, BlockchainRepository
)
from migrations.migration_manager import MigrationManager, SeedDataManager
from firestore_db import write_data_to_firestore, write_wallet_address_to_firestore
from schema import DataModel, EventModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    try:
        await db_manager.initialize()
        logger.info("Database connections initialized")
        yield
    finally:
        # Shutdown
        await db_manager.close()
        logger.info("Database connections closed")

app = FastAPI(
    title="The Construct Data Storage Service",
    description="Blockchain layer data storage with PostgreSQL, Redis, and Firestore",
    version="1.0.0",
    lifespan=lifespan
)

baseUrl = os.getenv("_BASEURL")
defaultUrl = os.getenv("_DEFAULT_URL")

# Enable CORS for all origins (testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Repository dependencies
async def get_user_repository() -> UserRepository:
    return UserRepository(db_manager)

async def get_asset_repository() -> AssetRepository:
    return AssetRepository(db_manager)

async def get_trading_repository() -> TradingRepository:
    return TradingRepository(db_manager)

async def get_manufacturing_repository() -> ManufacturingRepository:
    return ManufacturingRepository(db_manager)

async def get_governance_repository() -> GovernanceRepository:
    return GovernanceRepository(db_manager)

async def get_blockchain_repository() -> BlockchainRepository:
    return BlockchainRepository(db_manager)

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        health_status = await db_manager.health_check()
        if health_status['overall']:
            return {"status": "healthy", "databases": health_status}
        else:
            return JSONResponse(
                status_code=503,
                content={"status": "unhealthy", "databases": health_status}
            )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "message": str(e)}
        )

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        health_status = await db_manager.health_check()
        if health_status['postgresql'] and health_status['redis']:
            return {"status": "ready"}
        else:
            return JSONResponse(
                status_code=503,
                content={"status": "not_ready", "databases": health_status}
            )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "message": str(e)}
        )

# Legacy Firestore endpoints (for backward compatibility)
@app.post("/saveAddress")
async def save_address(request: DataModel):
    """Saves a wallet address to Firestore (legacy endpoint)"""
    try:
        # Extract the wallet address from the body
        wallet_address = request

        # Write the wallet address to Firestore
        response = write_wallet_address_to_firestore(wallet_address)

        return {"message": response}
    except Exception as e:
        return {"error": str(e)}

@app.post("/saveData")
async def save_data(request: EventModel):
    """Saves data to Firestore (legacy endpoint)"""
    try:
        # Write data to database
        response = write_data_to_firestore(request)
        return response
    except Exception as e:
        return {"error": str(e)}

# User management endpoints
@app.get("/api/users/{user_id}")
async def get_user(user_id: str, user_repo: UserRepository = Depends(get_user_repository)):
    """Get user by ID"""
    try:
        from uuid import UUID
        user = await user_repo.get_by_id(UUID(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/wallet/{wallet_address}")
async def get_user_by_wallet(wallet_address: str, user_repo: UserRepository = Depends(get_user_repository)):
    """Get user by wallet address"""
    try:
        user = await user_repo.get_by_wallet_address(wallet_address)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/{user_id}/stats")
async def get_user_stats(user_id: str, user_repo: UserRepository = Depends(get_user_repository)):
    """Get comprehensive user statistics"""
    try:
        from uuid import UUID
        stats = await user_repo.get_user_stats(UUID(user_id))
        return stats
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Asset management endpoints
@app.get("/api/assets/{asset_id}")
async def get_asset(asset_id: str, asset_repo: AssetRepository = Depends(get_asset_repository)):
    """Get asset by ID"""
    try:
        from uuid import UUID
        asset = await asset_repo.get_by_id(UUID(asset_id))
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid asset ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/assets/search")
async def search_assets(q: str, asset_type: str = None, limit: int = 20, 
                       asset_repo: AssetRepository = Depends(get_asset_repository)):
    """Search assets"""
    try:
        assets = await asset_repo.search_assets(q, asset_type, limit)
        return {"assets": assets, "total": len(assets)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Trading endpoints
@app.get("/api/trading/orders/{order_id}")
async def get_order(order_id: str, trading_repo: TradingRepository = Depends(get_trading_repository)):
    """Get trading order by ID"""
    try:
        from uuid import UUID
        order = await trading_repo.get_order_by_id(UUID(order_id))
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trading/orderbook/{asset_id}")
async def get_order_book(asset_id: str, limit: int = 50, 
                        trading_repo: TradingRepository = Depends(get_trading_repository)):
    """Get order book for an asset"""
    try:
        from uuid import UUID
        order_book = await trading_repo.get_order_book(UUID(asset_id), limit)
        return order_book
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid asset ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Manufacturing endpoints
@app.get("/api/manufacturing/orders/{order_id}")
async def get_manufacturing_order(order_id: str, 
                                 mfg_repo: ManufacturingRepository = Depends(get_manufacturing_repository)):
    """Get manufacturing order by ID"""
    try:
        from uuid import UUID
        order = await mfg_repo.get_order_by_id(UUID(order_id))
        if not order:
            raise HTTPException(status_code=404, detail="Manufacturing order not found")
        return order
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/manufacturing/orders/{order_id}/progress")
async def get_order_progress(order_id: str, 
                           mfg_repo: ManufacturingRepository = Depends(get_manufacturing_repository)):
    """Get manufacturing order progress"""
    try:
        from uuid import UUID
        progress = await mfg_repo.get_order_progress(UUID(order_id))
        return progress
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Governance endpoints
@app.get("/api/governance/proposals/active")
async def get_active_proposals(limit: int = 50, 
                              gov_repo: GovernanceRepository = Depends(get_governance_repository)):
    """Get active governance proposals"""
    try:
        proposals = await gov_repo.get_active_proposals(limit)
        return {"proposals": proposals, "total": len(proposals)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/governance/proposals/{proposal_id}")
async def get_proposal(proposal_id: str, 
                      gov_repo: GovernanceRepository = Depends(get_governance_repository)):
    """Get governance proposal by ID"""
    try:
        from uuid import UUID
        proposal = await gov_repo.get_proposal_by_id(UUID(proposal_id))
        if not proposal:
            raise HTTPException(status_code=404, detail="Proposal not found")
        return proposal
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid proposal ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Blockchain endpoints
@app.get("/api/blockchain/transactions/{tx_hash}")
async def get_transaction(tx_hash: str, 
                         blockchain_repo: BlockchainRepository = Depends(get_blockchain_repository)):
    """Get transaction by hash"""
    try:
        transaction = await blockchain_repo.get_transaction_by_hash(tx_hash)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blockchain/prices/{asset_symbol}")
async def get_latest_price(asset_symbol: str, source: str = None,
                          blockchain_repo: BlockchainRepository = Depends(get_blockchain_repository)):
    """Get latest price for an asset"""
    try:
        price = await blockchain_repo.get_latest_price(asset_symbol, source)
        if not price:
            raise HTTPException(status_code=404, detail="Price not found")
        return price
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoints
@app.get("/api/analytics/market")
async def get_market_analytics(asset_id: str = None,
                              trading_repo: TradingRepository = Depends(get_trading_repository)):
    """Get market analytics"""
    try:
        from uuid import UUID
        asset_uuid = UUID(asset_id) if asset_id else None
        analytics = await trading_repo.get_market_summary(asset_uuid)
        return analytics
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid asset ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/manufacturing")
async def get_manufacturing_analytics(days: int = 30,
                                     mfg_repo: ManufacturingRepository = Depends(get_manufacturing_repository)):
    """Get manufacturing analytics"""
    try:
        analytics = await mfg_repo.get_manufacturing_analytics(days)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Migration and maintenance endpoints
@app.post("/api/admin/migrate")
async def run_migrations():
    """Run database migrations"""
    try:
        migration_manager = MigrationManager(db_manager.pg_config)
        result = await migration_manager.run_migrations()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/seed")
async def seed_database():
    """Seed database with test data"""
    try:
        seed_manager = SeedDataManager(db_manager.pg_config)
        result = await seed_manager.seed_database()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/migration-status")
async def get_migration_status():
    """Get migration status"""
    try:
        migration_manager = MigrationManager(db_manager.pg_config)
        status = await migration_manager.get_migration_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    """Return a friendly HTTP greeting."""
    message = "The Construct Data Storage Service is running!"

    return templates.TemplateResponse(
        "index.html", {"request": request, "message": message}
    )

# Execute the application when the script is run
if __name__ == "__main__":
    # Get the server port from the environment variable
    server_port = os.environ.get("PORT", "8080")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=int(server_port))
