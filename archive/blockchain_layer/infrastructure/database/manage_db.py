#!/usr/bin/env python3
"""
Database management CLI utility for The Construct blockchain layer
"""
import asyncio
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent.parent.parent / "core" / "data_storage" / "app"
sys.path.insert(0, str(app_dir))

from database import DatabaseManager
from migrations.migration_manager import MigrationManager, SeedDataManager

async def setup_database_manager():
    """Setup database manager with configuration"""
    db_config = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': int(os.getenv('POSTGRES_PORT', 5432)),
        'database': os.getenv('POSTGRES_DB', 'the_construct'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'password')
    }
    return DatabaseManager(), db_config

async def migrate_command(args):
    """Run database migrations"""
    print("🚀 Running database migrations...")
    
    db_manager, db_config = await setup_database_manager()
    migration_manager = MigrationManager(db_config)
    
    try:
        result = await migration_manager.run_migrations(args.migrations_dir)
        
        print(f"✅ Migration completed successfully!")
        print(f"   Applied: {result['applied_migrations']} migrations")
        print(f"   Skipped: {result['skipped_migrations']} migrations")
        print(f"   Total: {result['total_migrations']} migrations")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

async def seed_command(args):
    """Seed database with test data"""
    print("🌱 Seeding database with test data...")
    
    db_manager, db_config = await setup_database_manager()
    seed_manager = SeedDataManager(db_config)
    
    try:
        result = await seed_manager.seed_database(args.seed_file)
        
        print(f"✅ Database seeded successfully!")
        print("   Statistics:")
        for table, count in result['statistics'].items():
            print(f"     {table}: {count} records")
        
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        sys.exit(1)

async def status_command(args):
    """Show migration status"""
    print("📊 Checking migration status...")
    
    db_manager, db_config = await setup_database_manager()
    migration_manager = MigrationManager(db_config)
    
    try:
        status = await migration_manager.get_migration_status()
        
        print(f"✅ Migration status:")
        print(f"   Total applied: {status['total_applied']} migrations")
        
        if status['last_migration']:
            last = status['last_migration']
            print(f"   Last migration: {last['name']}")
            print(f"   Applied at: {last['applied_at']}")
        
        if args.verbose:
            print("\n   Applied migrations:")
            for migration in status['applied_migrations']:
                print(f"     - {migration['name']} ({migration['applied_at']})")
        
    except Exception as e:
        print(f"❌ Status check failed: {e}")
        sys.exit(1)

async def validate_command(args):
    """Validate migration integrity"""
    print("🔍 Validating migration integrity...")
    
    db_manager, db_config = await setup_database_manager()
    migration_manager = MigrationManager(db_config)
    
    try:
        validation = await migration_manager.validate_migrations(args.migrations_dir)
        
        print(f"✅ Validation completed:")
        print(f"   Total migrations: {validation['total_migrations']}")
        print(f"   Valid: {validation['valid_migrations']}")
        print(f"   Invalid: {validation['invalid_migrations']}")
        print(f"   Pending: {validation['pending_migrations']}")
        
        if validation['invalid_migrations'] > 0:
            print("\n❌ Invalid migrations found:")
            for result in validation['results']:
                if not result['valid']:
                    print(f"     - {result['migration']}: {result['status']}")
        
        if args.verbose:
            print("\n   All migration results:")
            for result in validation['results']:
                status_icon = "✅" if result['valid'] else "❌"
                print(f"     {status_icon} {result['migration']}: {result['status']}")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)

async def backup_command(args):
    """Create database backup"""
    print("💾 Creating database backup...")
    
    db_manager, db_config = await setup_database_manager()
    seed_manager = SeedDataManager(db_config)
    
    # Generate backup filename if not provided
    if not args.backup_file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.backup_file = f"backup_{timestamp}.json"
    
    try:
        result = await seed_manager.backup_data(args.backup_file)
        
        print(f"✅ Backup created successfully!")
        print(f"   File: {result['backup_file']}")
        print(f"   Records: {result['total_records']}")
        print(f"   Tables: {result['tables_backed_up']}")
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        sys.exit(1)

async def restore_command(args):
    """Restore database from backup"""
    print(f"🔄 Restoring database from {args.backup_file}...")
    
    if not os.path.exists(args.backup_file):
        print(f"❌ Backup file not found: {args.backup_file}")
        sys.exit(1)
    
    # Confirm restoration
    if not args.force:
        response = input("⚠️  This will clear all existing data. Continue? (y/N): ")
        if response.lower() != 'y':
            print("Restoration cancelled.")
            return
    
    db_manager, db_config = await setup_database_manager()
    seed_manager = SeedDataManager(db_config)
    
    try:
        result = await seed_manager.restore_data(args.backup_file)
        
        print(f"✅ Database restored successfully!")
        print(f"   File: {result['backup_file']}")
        print(f"   Records restored: {result['restored_records']}")
        
    except Exception as e:
        print(f"❌ Restoration failed: {e}")
        sys.exit(1)

async def clear_command(args):
    """Clear test data from database"""
    print("🧹 Clearing test data...")
    
    # Confirm clearing
    if not args.force:
        response = input("⚠️  This will delete all data. Continue? (y/N): ")
        if response.lower() != 'y':
            print("Clear operation cancelled.")
            return
    
    db_manager, db_config = await setup_database_manager()
    seed_manager = SeedDataManager(db_config)
    
    try:
        result = await seed_manager.clear_test_data()
        
        print(f"✅ Test data cleared successfully!")
        print("   Cleared records:")
        for table, count in result['cleared_records'].items():
            if count > 0:
                print(f"     {table}: {count} records")
        
    except Exception as e:
        print(f"❌ Clear operation failed: {e}")
        sys.exit(1)

async def health_command(args):
    """Check database health"""
    print("🏥 Checking database health...")
    
    db_manager, db_config = await setup_database_manager()
    
    try:
        await db_manager.initialize()
        health_status = await db_manager.health_check()
        
        print(f"✅ Health check completed:")
        print(f"   PostgreSQL: {'✅' if health_status['postgresql'] else '❌'}")
        print(f"   Redis: {'✅' if health_status['redis'] else '❌'}")
        print(f"   Firestore: {'✅' if health_status['firestore'] else '❌'}")
        print(f"   Overall: {'✅ Healthy' if health_status['overall'] else '❌ Unhealthy'}")
        
        if not health_status['overall']:
            sys.exit(1)
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)
    finally:
        await db_manager.close()

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Database management utility for The Construct blockchain layer"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', help='Run database migrations')
    migrate_parser.add_argument(
        '--migrations-dir', 
        default=None,
        help='Directory containing migration files'
    )
    
    # Seed command
    seed_parser = subparsers.add_parser('seed', help='Seed database with test data')
    seed_parser.add_argument(
        '--seed-file',
        default=None,
        help='Path to seed data file'
    )
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show migration status')
    status_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed migration information'
    )
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate migration integrity')
    validate_parser.add_argument(
        '--migrations-dir',
        default=None,
        help='Directory containing migration files'
    )
    validate_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed validation results'
    )
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create database backup')
    backup_parser.add_argument(
        '--backup-file',
        default=None,
        help='Backup file path (auto-generated if not provided)'
    )
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore database from backup')
    restore_parser.add_argument(
        'backup_file',
        help='Backup file to restore from'
    )
    restore_parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Skip confirmation prompt'
    )
    
    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear all test data')
    clear_parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Skip confirmation prompt'
    )
    
    # Health command
    health_parser = subparsers.add_parser('health', help='Check database health')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Load environment variables
    from dotenv import load_dotenv
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
    
    # Execute command
    command_map = {
        'migrate': migrate_command,
        'seed': seed_command,
        'status': status_command,
        'validate': validate_command,
        'backup': backup_command,
        'restore': restore_command,
        'clear': clear_command,
        'health': health_command
    }
    
    if args.command in command_map:
        asyncio.run(command_map[args.command](args))
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
