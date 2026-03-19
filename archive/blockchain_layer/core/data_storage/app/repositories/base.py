"""
Base repository class with caching and common database operations
"""
import json
import hashlib
from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import asyncpg
import redis.asyncio as redis
from google.cloud import firestore
import logging

logger = logging.getLogger(__name__)

class BaseRepository(ABC):
    """Base repository class with caching capabilities"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.cache_ttl = 300  # 5 minutes default cache TTL
        
    def _generate_cache_key(self, prefix: str, *args) -> str:
        """Generate a cache key from prefix and arguments"""
        key_data = f"{prefix}:{':'.join(str(arg) for arg in args)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get data from Redis cache"""
        try:
            redis_client = await self.db_manager.get_redis_client()
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"Cache read failed for key {cache_key}: {e}")
        return None
    
    async def _set_cache(self, cache_key: str, data: Any, ttl: Optional[int] = None) -> None:
        """Set data in Redis cache"""
        try:
            redis_client = await self.db_manager.get_redis_client()
            ttl = ttl or self.cache_ttl
            await redis_client.setex(
                cache_key, 
                ttl, 
                json.dumps(data, default=str)
            )
        except Exception as e:
            logger.warning(f"Cache write failed for key {cache_key}: {e}")
    
    async def _invalidate_cache(self, pattern: str) -> None:
        """Invalidate cache entries matching pattern"""
        try:
            redis_client = await self.db_manager.get_redis_client()
            keys = await redis_client.keys(pattern)
            if keys:
                await redis_client.delete(*keys)
        except Exception as e:
            logger.warning(f"Cache invalidation failed for pattern {pattern}: {e}")
    
    async def _execute_query(self, query: str, *args) -> List[Dict[str, Any]]:
        """Execute a PostgreSQL query and return results"""
        async with self.db_manager.get_pg_connection() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
    
    async def _execute_query_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Execute a PostgreSQL query and return single result"""
        async with self.db_manager.get_pg_connection() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None
    
    async def _execute_command(self, query: str, *args) -> str:
        """Execute a PostgreSQL command and return status"""
        async with self.db_manager.get_pg_connection() as conn:
            return await conn.execute(query, *args)
    
    async def _backup_to_firestore(self, collection: str, document_id: str, data: Dict[str, Any]) -> None:
        """Backup data to Firestore for redundancy"""
        try:
            firestore_client = self.db_manager.get_firestore_client()
            doc_ref = firestore_client.collection(collection).document(document_id)
            doc_ref.set({
                **data,
                'backup_timestamp': firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            logger.warning(f"Firestore backup failed for {collection}/{document_id}: {e}")

class CachedQuery:
    """Decorator for caching query results"""
    
    def __init__(self, cache_key_prefix: str, ttl: int = 300):
        self.cache_key_prefix = cache_key_prefix
        self.ttl = ttl
    
    def __call__(self, func):
        async def wrapper(self, *args, **kwargs):
            # Generate cache key
            cache_key = self._generate_cache_key(self.cache_key_prefix, *args, **kwargs)
            
            # Try to get from cache first
            cached_result = await self._get_from_cache(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute the function
            result = await func(self, *args, **kwargs)
            
            # Cache the result
            if result is not None:
                await self._set_cache(cache_key, result, self.ttl)
            
            return result
        return wrapper

class TransactionManager:
    """Manages database transactions across multiple operations"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.connection = None
        self.transaction = None
    
    async def __aenter__(self):
        self.connection = await self.db_manager.pg_pool.acquire()
        self.transaction = self.connection.transaction()
        await self.transaction.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                await self.transaction.commit()
            else:
                await self.transaction.rollback()
        finally:
            await self.db_manager.pg_pool.release(self.connection)
    
    async def execute(self, query: str, *args):
        """Execute query within transaction"""
        return await self.connection.execute(query, *args)
    
    async def fetch(self, query: str, *args):
        """Fetch results within transaction"""
        rows = await self.connection.fetch(query, *args)
        return [dict(row) for row in rows]
    
    async def fetchrow(self, query: str, *args):
        """Fetch single row within transaction"""
        row = await self.connection.fetchrow(query, *args)
        return dict(row) if row else None
