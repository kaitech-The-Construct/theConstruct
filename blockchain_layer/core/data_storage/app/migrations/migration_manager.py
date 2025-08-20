"""
Database migration manager for The Construct blockchain layer
"""
import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncpg
import logging

logger = logging.getLogger(__name__)

class MigrationManager:
    """Manages database schema migrations"""
    
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        self.migrations_table = 'schema_migrations'
        
    async def _get_connection(self):
        """Get database connection"""
        return await asyncpg.connect(
            host=self.db_config['host'],
            port=self.db_config['port'],
            database=self.db_config['database'],
            user=self.db_config['user'],
            password=self.db_config['password']
        )
    
    async def _ensure_migrations_table(self, conn):
        """Ensure the migrations tracking table exists"""
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id SERIAL PRIMARY KEY,
                migration_name VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                checksum VARCHAR(64) NOT NULL
            )
        """)
    
    async def _get_applied_migrations(self, conn) -> List[str]:
        """Get list of applied migration names"""
        rows = await conn.fetch("""
            SELECT migration_name FROM schema_migrations ORDER BY applied_at
        """)
        return [row['migration_name'] for row in rows]
    
    async def _calculate_checksum(self, migration_content: str) -> str:
        """Calculate checksum for migration content"""
        import hashlib
        return hashlib.sha256(migration_content.encode()).hexdigest()
    
    async def _load_migration_file(self, migration_path: str) -> str:
        """Load migration file content"""
        with open(migration_path, 'r') as f:
            return f.read()
    
    async def _apply_migration(self, conn, migration_name: str, migration_content: str):
        """Apply a single migration"""
        try:
            # Execute migration SQL
            await conn.execute(migration_content)
            
            # Record migration as applied
            checksum = await self._calculate_checksum(migration_content)
            await conn.execute("""
                INSERT INTO schema_migrations (migration_name, checksum)
                VALUES ($1, $2)
            """, migration_name, checksum)
            
            logger.info(f"Applied migration: {migration_name}")
            
        except Exception as e:
            logger.error(f"Failed to apply migration {migration_name}: {e}")
            raise
    
    async def run_migrations(self, migrations_dir: str = None) -> Dict[str, Any]:
        """Run all pending migrations"""
        if not migrations_dir:
            migrations_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'infrastructure', 'database', 'init')
        
        conn = await self._get_connection()
        
        try:
            # Ensure migrations table exists
            await self._ensure_migrations_table(conn)
            
            # Get applied migrations
            applied_migrations = await self._get_applied_migrations(conn)
            
            # Get available migration files
            migration_files = []
            if os.path.exists(migrations_dir):
                for filename in sorted(os.listdir(migrations_dir)):
                    if filename.endswith('.sql'):
                        migration_files.append(filename)
            
            # Apply pending migrations
            applied_count = 0
            skipped_count = 0
            
            for migration_file in migration_files:
                migration_name = migration_file[:-4]  # Remove .sql extension
                
                if migration_name in applied_migrations:
                    skipped_count += 1
                    logger.info(f"Skipping already applied migration: {migration_name}")
                    continue
                
                migration_path = os.path.join(migrations_dir, migration_file)
                migration_content = await self._load_migration_file(migration_path)
                
                await self._apply_migration(conn, migration_name, migration_content)
                applied_count += 1
            
            return {
                'applied_migrations': applied_count,
                'skipped_migrations': skipped_count,
                'total_migrations': len(applied_migrations) + applied_count
            }
            
        finally:
            await conn.close()
    
    async def rollback_migration(self, migration_name: str, rollback_sql: str) -> bool:
        """Rollback a specific migration"""
        conn = await self._get_connection()
        
        try:
            # Check if migration was applied
            applied_migrations = await self._get_applied_migrations(conn)
            
            if migration_name not in applied_migrations:
                logger.warning(f"Migration {migration_name} was not applied, cannot rollback")
                return False
            
            # Execute rollback SQL
            await conn.execute(rollback_sql)
            
            # Remove migration record
            await conn.execute("""
                DELETE FROM schema_migrations WHERE migration_name = $1
            """, migration_name)
            
            logger.info(f"Rolled back migration: {migration_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to rollback migration {migration_name}: {e}")
            raise
        finally:
            await conn.close()
    
    async def get_migration_status(self) -> Dict[str, Any]:
        """Get current migration status"""
        conn = await self._get_connection()
        
        try:
            await self._ensure_migrations_table(conn)
            
            # Get applied migrations with details
            rows = await conn.fetch("""
                SELECT migration_name, applied_at, checksum
                FROM schema_migrations 
                ORDER BY applied_at DESC
            """)
            
            applied_migrations = [
                {
                    'name': row['migration_name'],
                    'applied_at': row['applied_at'],
                    'checksum': row['checksum']
                }
                for row in rows
            ]
            
            return {
                'total_applied': len(applied_migrations),
                'applied_migrations': applied_migrations,
                'last_migration': applied_migrations[0] if applied_migrations else None
            }
            
        finally:
            await conn.close()
    
    async def validate_migrations(self, migrations_dir: str = None) -> Dict[str, Any]:
        """Validate migration integrity"""
        if not migrations_dir:
            migrations_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'infrastructure', 'database', 'init')
        
        conn = await self._get_connection()
        
        try:
            await self._ensure_migrations_table(conn)
            
            # Get applied migrations
            applied_rows = await conn.fetch("""
                SELECT migration_name, checksum FROM schema_migrations
            """)
            applied_checksums = {row['migration_name']: row['checksum'] for row in applied_rows}
            
            validation_results = []
            
            # Check each migration file
            if os.path.exists(migrations_dir):
                for filename in sorted(os.listdir(migrations_dir)):
                    if filename.endswith('.sql'):
                        migration_name = filename[:-4]
                        migration_path = os.path.join(migrations_dir, filename)
                        
                        # Calculate current checksum
                        migration_content = await self._load_migration_file(migration_path)
                        current_checksum = await self._calculate_checksum(migration_content)
                        
                        if migration_name in applied_checksums:
                            stored_checksum = applied_checksums[migration_name]
                            is_valid = current_checksum == stored_checksum
                            
                            validation_results.append({
                                'migration': migration_name,
                                'status': 'applied',
                                'valid': is_valid,
                                'current_checksum': current_checksum,
                                'stored_checksum': stored_checksum
                            })
                        else:
                            validation_results.append({
                                'migration': migration_name,
                                'status': 'pending',
                                'valid': True,
                                'current_checksum': current_checksum,
                                'stored_checksum': None
                            })
            
            # Check for orphaned migration records
            migration_files = {f[:-4] for f in os.listdir(migrations_dir) if f.endswith('.sql')} if os.path.exists(migrations_dir) else set()
            orphaned_migrations = set(applied_checksums.keys()) - migration_files
            
            for orphaned in orphaned_migrations:
                validation_results.append({
                    'migration': orphaned,
                    'status': 'orphaned',
                    'valid': False,
                    'current_checksum': None,
                    'stored_checksum': applied_checksums[orphaned]
                })
            
            return {
                'total_migrations': len(validation_results),
                'valid_migrations': len([r for r in validation_results if r['valid']]),
                'invalid_migrations': len([r for r in validation_results if not r['valid']]),
                'pending_migrations': len([r for r in validation_results if r['status'] == 'pending']),
                'results': validation_results
            }
            
        finally:
            await conn.close()

class SeedDataManager:
    """Manages database seed data"""
    
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
    
    async def _get_connection(self):
        """Get database connection"""
        return await asyncpg.connect(
            host=self.db_config['host'],
            port=self.db_config['port'],
            database=self.db_config['database'],
            user=self.db_config['user'],
            password=self.db_config['password']
        )
    
    async def seed_database(self, seed_file_path: str = None) -> Dict[str, Any]:
        """Seed database with test data"""
        if not seed_file_path:
            seed_file_path = os.path.join(
                os.path.dirname(__file__), '..', '..', 'infrastructure', 
                'database', 'init', '02_seed_data.sql'
            )
        
        if not os.path.exists(seed_file_path):
            raise FileNotFoundError(f"Seed file not found: {seed_file_path}")
        
        conn = await self._get_connection()
        
        try:
            # Load seed data
            with open(seed_file_path, 'r') as f:
                seed_sql = f.read()
            
            # Execute seed data
            await conn.execute(seed_sql)
            
            # Get seeding statistics
            stats = await self._get_seeding_stats(conn)
            
            logger.info("Database seeded successfully")
            return {
                'status': 'success',
                'statistics': stats
            }
            
        except Exception as e:
            logger.error(f"Failed to seed database: {e}")
            raise
        finally:
            await conn.close()
    
    async def _get_seeding_stats(self, conn) -> Dict[str, Any]:
        """Get statistics about seeded data"""
        stats = {}
        
        # Count records in each table
        tables = [
            ('blockchain.users', 'users'),
            ('blockchain.assets', 'assets'),
            ('trading.orders', 'orders'),
            ('trading.escrows', 'escrows'),
            ('manufacturing.orders', 'manufacturing_orders'),
            ('manufacturing.milestones', 'milestones'),
            ('manufacturing.quality_assurance', 'quality_records'),
            ('governance.proposals', 'proposals'),
            ('governance.votes', 'votes'),
            ('blockchain.transactions', 'transactions'),
            ('blockchain.price_feeds', 'price_feeds')
        ]
        
        for table_name, stat_key in tables:
            try:
                count = await conn.fetchval(f"SELECT COUNT(*) FROM {table_name}")
                stats[stat_key] = count
            except Exception as e:
                logger.warning(f"Could not get count for {table_name}: {e}")
                stats[stat_key] = 0
        
        return stats
    
    async def clear_test_data(self) -> Dict[str, Any]:
        """Clear all test data from database"""
        conn = await self._get_connection()
        
        try:
            # Get stats before clearing
            stats_before = await self._get_seeding_stats(conn)
            
            # Clear data in reverse dependency order
            clear_queries = [
                "DELETE FROM governance.votes",
                "DELETE FROM governance.proposals",
                "DELETE FROM manufacturing.quality_assurance",
                "DELETE FROM manufacturing.milestones",
                "DELETE FROM manufacturing.orders",
                "DELETE FROM trading.escrows",
                "DELETE FROM trading.orders",
                "DELETE FROM blockchain.transactions",
                "DELETE FROM blockchain.price_feeds",
                "DELETE FROM blockchain.assets",
                "DELETE FROM blockchain.users"
            ]
            
            for query in clear_queries:
                await conn.execute(query)
            
            # Reset sequences
            sequence_queries = [
                "SELECT setval('blockchain.users_id_seq', 1, false)",
                "SELECT setval('blockchain.assets_id_seq', 1, false)",
                "SELECT setval('trading.orders_id_seq', 1, false)",
                "SELECT setval('trading.escrows_id_seq', 1, false)",
                "SELECT setval('manufacturing.orders_id_seq', 1, false)",
                "SELECT setval('manufacturing.milestones_id_seq', 1, false)",
                "SELECT setval('manufacturing.quality_assurance_id_seq', 1, false)",
                "SELECT setval('governance.proposals_id_seq', 1, false)",
                "SELECT setval('governance.votes_id_seq', 1, false)",
                "SELECT setval('blockchain.transactions_id_seq', 1, false)",
                "SELECT setval('blockchain.price_feeds_id_seq', 1, false)"
            ]
            
            for query in sequence_queries:
                try:
                    await conn.execute(query)
                except Exception as e:
                    logger.warning(f"Could not reset sequence: {e}")
            
            logger.info("Test data cleared successfully")
            return {
                'status': 'success',
                'cleared_records': stats_before
            }
            
        except Exception as e:
            logger.error(f"Failed to clear test data: {e}")
            raise
        finally:
            await conn.close()
    
    async def backup_data(self, backup_file: str) -> Dict[str, Any]:
        """Create a backup of current data"""
        conn = await self._get_connection()
        
        try:
            # Get all data
            backup_data = {}
            
            tables = [
                'blockchain.users',
                'blockchain.assets', 
                'trading.orders',
                'trading.escrows',
                'manufacturing.orders',
                'manufacturing.milestones',
                'manufacturing.quality_assurance',
                'governance.proposals',
                'governance.votes',
                'blockchain.transactions',
                'blockchain.price_feeds'
            ]
            
            for table in tables:
                rows = await conn.fetch(f"SELECT * FROM {table}")
                backup_data[table] = [dict(row) for row in rows]
            
            # Save to file
            import json
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, default=str, indent=2)
            
            # Get backup statistics
            total_records = sum(len(data) for data in backup_data.values())
            
            logger.info(f"Data backup created: {backup_file}")
            return {
                'status': 'success',
                'backup_file': backup_file,
                'total_records': total_records,
                'tables_backed_up': len(backup_data)
            }
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise
        finally:
            await conn.close()
    
    async def restore_data(self, backup_file: str) -> Dict[str, Any]:
        """Restore data from backup file"""
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"Backup file not found: {backup_file}")
        
        conn = await self._get_connection()
        
        try:
            # Load backup data
            import json
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            # Clear existing data first
            await self.clear_test_data()
            
            # Restore data in dependency order
            restore_order = [
                'blockchain.users',
                'blockchain.assets',
                'trading.orders',
                'trading.escrows', 
                'manufacturing.orders',
                'manufacturing.milestones',
                'manufacturing.quality_assurance',
                'governance.proposals',
                'governance.votes',
                'blockchain.transactions',
                'blockchain.price_feeds'
            ]
            
            restored_records = 0
            
            for table in restore_order:
                if table in backup_data:
                    records = backup_data[table]
                    
                    if records:
                        # Build insert query
                        first_record = records[0]
                        columns = list(first_record.keys())
                        placeholders = ', '.join([f'${i+1}' for i in range(len(columns))])
                        
                        insert_query = f"""
                            INSERT INTO {table} ({', '.join(columns)})
                            VALUES ({placeholders})
                        """
                        
                        # Insert records
                        for record in records:
                            values = [record[col] for col in columns]
                            await conn.execute(insert_query, *values)
                            restored_records += 1
            
            logger.info(f"Data restored from backup: {backup_file}")
            return {
                'status': 'success',
                'restored_records': restored_records,
                'backup_file': backup_file
            }
            
        except Exception as e:
            logger.error(f"Failed to restore data: {e}")
            raise
        finally:
            await conn.close()
    
    async def create_migration_file(self, migration_name: str, migration_sql: str, migrations_dir: str = None) -> str:
        """Create a new migration file"""
        if not migrations_dir:
            migrations_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'infrastructure', 'database', 'migrations')
        
        # Ensure migrations directory exists
        os.makedirs(migrations_dir, exist_ok=True)
        
        # Generate timestamp prefix
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{migration_name}.sql"
        filepath = os.path.join(migrations_dir, filename)
        
        # Write migration file
        with open(filepath, 'w') as f:
            f.write(f"-- Migration: {migration_name}\n")
            f.write(f"-- Created: {datetime.now().isoformat()}\n\n")
            f.write(migration_sql)
        
        logger.info(f"Created migration file: {filepath}")
        return filepath
