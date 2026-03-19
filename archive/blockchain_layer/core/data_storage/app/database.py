"""
Database connection and configuration management
"""
import os
import asyncio
from typing import Optional, Dict, Any
import asyncpg
import redis.asyncio as redis
from google.cloud import firestore
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages connections to PostgreSQL, Redis, and Firestore"""
    
    def __init__(self):
        self.pg_pool: Optional[asyncpg.Pool] = None
        self.redis_client: Optional[redis.Redis] = None
        self.firestore_client: Optional[firestore.Client] = None
        
        # Database configuration
        self.pg_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'the_construct'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', 'password'),
            'min_size': int(os.getenv('POSTGRES_MIN_POOL_SIZE', 5)),
            'max_size': int(os.getenv('POSTGRES_MAX_POOL_SIZE', 20))
        }
        
        self.redis_config = {
            'host': os.getenv('REDIS_HOST', 'localhost'),
            'port': int(os.getenv('REDIS_PORT', 6379)),
            'password': os.getenv('REDIS_PASSWORD', None),
            'db': int(os.getenv('REDIS_DB', 0)),
            'decode_responses': True
        }
    
    async def initialize(self):
        """Initialize all database connections"""
        try:
            # Initialize PostgreSQL connection pool
            self.pg_pool = await asyncpg.create_pool(
                host=self.pg_config['host'],
                port=self.pg_config['port'],
                database=self.pg_config['database'],
                user=self.pg_config['user'],
                password=self.pg_config['password'],
                min_size=self.pg_config['min_size'],
                max_size=self.pg_config['max_size']
            )
            logger.info("PostgreSQL connection pool initialized")
            
            # Initialize Redis connection
            self.redis_client = redis.Redis(
                host=self.redis_config['host'],
                port=self.redis_config['port'],
                password=self.redis_config['password'],
                db=self.redis_config['db'],
                decode_responses=self.redis_config['decode_responses']
            )
            await self.redis_client.ping()
            logger.info("Redis connection initialized")
            
            # Initialize Firestore client
            self.firestore_client = firestore.Client()
            logger.info("Firestore client initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    async def close(self):
        """Close all database connections"""
        if self.pg_pool:
            await self.pg_pool.close()
            logger.info("PostgreSQL connection pool closed")
        
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis connection closed")
        
        if self.firestore_client:
            # Firestore client doesn't need explicit closing
            logger.info("Firestore client closed")
    
    @asynccontextmanager
    async def get_pg_connection(self):
        """Get a PostgreSQL connection from the pool"""
        if not self.pg_pool:
            raise RuntimeError("PostgreSQL pool not initialized")
        
        async with self.pg_pool.acquire() as connection:
            yield connection
    
    async def get_redis_client(self) -> redis.Redis:
        """Get Redis client"""
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        return self.redis_client
    
    def get_firestore_client(self) -> firestore.Client:
        """Get Firestore client"""
        if not self.firestore_client:
            raise RuntimeError("Firestore client not initialized")
        return self.firestore_client
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all database connections"""
        health_status = {
            'postgresql': False,
            'redis': False,
            'firestore': False,
            'overall': False
        }
        
        try:
            # Check PostgreSQL
            if self.pg_pool:
                async with self.get_pg_connection() as conn:
                    await conn.fetchval('SELECT 1')
                health_status['postgresql'] = True
        except Exception as e:
            logger.error(f"PostgreSQL health check failed: {e}")
        
        try:
            # Check Redis
            if self.redis_client:
                await self.redis_client.ping()
                health_status['redis'] = True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
        
        try:
            # Check Firestore
            if self.firestore_client:
                # Simple read operation to test connection
                test_ref = self.firestore_client.collection('health_check').document('test')
                test_ref.set({'timestamp': firestore.SERVER_TIMESTAMP})
                health_status['firestore'] = True
        except Exception as e:
            logger.error(f"Firestore health check failed: {e}")
        
        health_status['overall'] = all([
            health_status['postgresql'],
            health_status['redis'],
            health_status['firestore']
        ])
        
        return health_status

# Global database manager instance
db_manager = DatabaseManager()
