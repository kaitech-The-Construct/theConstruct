# The Construct Database Schema Implementation

This directory contains the complete database schema implementation for The Construct blockchain layer, including PostgreSQL schema, Redis caching, Firestore integration, and comprehensive data access layers.

## Architecture Overview

The database layer implements a multi-database architecture:

- **PostgreSQL**: Primary relational database for structured data
- **Redis**: High-performance caching layer
- **Firestore**: Document database for backup and real-time features

## Database Schema

### Schema Organization

The PostgreSQL database is organized into four schemas:

1. **blockchain**: Core blockchain entities (users, assets, transactions, price feeds)
2. **trading**: Trading-related entities (orders, escrows)
3. **manufacturing**: Manufacturing workflow entities (orders, milestones, quality assurance)
4. **governance**: Governance entities (proposals, votes)

### Key Tables

#### Blockchain Schema
- `users`: User accounts with wallet addresses and reputation scores
- `assets`: Tokenized robotics components with specifications
- `transactions`: Blockchain transaction records
- `price_feeds`: Real-time price data from oracles

#### Trading Schema
- `orders`: Buy/sell orders for tokenized assets
- `escrows`: Escrow contracts for secure transactions

#### Manufacturing Schema
- `orders`: Manufacturing orders with custom specifications
- `milestones`: Payment milestones for manufacturing orders
- `quality_assurance`: Quality inspection records

#### Governance Schema
- `proposals`: Community governance proposals
- `votes`: Voting records for proposals

## Data Access Layer

### Repository Pattern

The data access layer implements the repository pattern with the following features:

- **Caching**: Automatic Redis caching with configurable TTL
- **Transactions**: Database transaction management
- **Backup**: Automatic Firestore backup for critical operations
- **Type Safety**: Full type hints and validation

### Available Repositories

1. **UserRepository**: User management and reputation tracking
2. **AssetRepository**: Tokenized asset management
3. **TradingRepository**: Order book and escrow management
4. **ManufacturingRepository**: Manufacturing workflow management
5. **GovernanceRepository**: Proposal and voting management
6. **BlockchainRepository**: Transaction and price feed management

## Quick Start

### 1. Environment Setup

Copy the environment template:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```bash
# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=the_construct
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Firestore Configuration
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
GOOGLE_CLOUD_PROJECT=your-project-id
```

### 2. Start Database Services

Using Docker Compose:
```bash
docker-compose up -d postgres redis
```

Wait for services to be healthy:
```bash
docker-compose ps
```

### 3. Run Migrations

Initialize the database schema:
```bash
python manage_db.py migrate
```

### 4. Seed Test Data

Load test data for development:
```bash
python manage_db.py seed
```

### 5. Start Data Storage Service

```bash
docker-compose up -d data_storage_service
```

## Database Management

### Migration Management

Check migration status:
```bash
python manage_db.py status
```

Validate migration integrity:
```bash
python manage_db.py validate --verbose
```

### Data Management

Create a backup:
```bash
python manage_db.py backup --backup-file my_backup.json
```

Restore from backup:
```bash
python manage_db.py restore my_backup.json
```

Clear all test data:
```bash
python manage_db.py clear --force
```

### Health Monitoring

Check database health:
```bash
python manage_db.py health
```

Or via HTTP endpoint:
```bash
curl http://localhost:8003/health
```

## API Endpoints

The data storage service provides RESTful APIs for all repositories:

### Health Endpoints
- `GET /health` - Comprehensive health check
- `GET /ready` - Readiness check for load balancers

### User Management
- `GET /api/users/{user_id}` - Get user by ID
- `GET /api/users/wallet/{wallet_address}` - Get user by wallet
- `GET /api/users/{user_id}/stats` - Get user statistics

### Asset Management
- `GET /api/assets/{asset_id}` - Get asset by ID
- `GET /api/assets/search?q={query}&asset_type={type}` - Search assets

### Trading
- `GET /api/trading/orders/{order_id}` - Get trading order
- `GET /api/trading/orderbook/{asset_id}` - Get order book

### Manufacturing
- `GET /api/manufacturing/orders/{order_id}` - Get manufacturing order
- `GET /api/manufacturing/orders/{order_id}/progress` - Get order progress

### Governance
- `GET /api/governance/proposals/active` - Get active proposals
- `GET /api/governance/proposals/{proposal_id}` - Get proposal details

### Blockchain
- `GET /api/blockchain/transactions/{tx_hash}` - Get transaction
- `GET /api/blockchain/prices/{asset_symbol}` - Get latest price

### Analytics
- `GET /api/analytics/market` - Market analytics
- `GET /api/analytics/manufacturing` - Manufacturing analytics

### Administration
- `POST /api/admin/migrate` - Run migrations
- `POST /api/admin/seed` - Seed database
- `GET /api/admin/migration-status` - Migration status

## Development Tools

### Database Administration

**PgAdmin** (PostgreSQL GUI):
- URL: http://localhost:5050
- Email: admin@theConstruct.dev
- Password: admin

**Redis Commander** (Redis GUI):
- URL: http://localhost:8081

### Performance Monitoring

The system includes comprehensive caching and performance monitoring:

- **Query Caching**: Automatic Redis caching for frequently accessed data
- **Cache Invalidation**: Smart cache invalidation on data updates
- **Connection Pooling**: PostgreSQL connection pooling for optimal performance
- **Health Checks**: Continuous health monitoring for all database services

## Caching Strategy

### Cache Layers

1. **Application Cache**: Redis-based caching with automatic invalidation
2. **Query Cache**: Cached query results with configurable TTL
3. **Connection Pool**: PostgreSQL connection pooling

### Cache TTL Configuration

- **User Data**: 10 minutes (600s)
- **Asset Data**: 5 minutes (300s)
- **Trading Data**: 1 minute (60s) - high volatility
- **Price Data**: 30 seconds - real-time requirements
- **Analytics**: 30 minutes (1800s)

### Cache Invalidation

The system automatically invalidates cache entries when:
- Related data is updated
- Transactions are completed
- User reputation changes
- Orders are filled or cancelled

## Security Features

### Data Protection

- **Connection Security**: SSL/TLS encryption for all database connections
- **Access Control**: Role-based access control for database operations
- **Input Validation**: Comprehensive input validation and sanitization
- **SQL Injection Prevention**: Parameterized queries throughout

### Backup Strategy

- **Automatic Backup**: Critical operations automatically backup to Firestore
- **Manual Backup**: CLI tools for creating and restoring backups
- **Data Redundancy**: Multi-database architecture for data redundancy

## Performance Optimization

### Database Indexes

The schema includes optimized indexes for:
- User lookups by wallet address
- Asset searches by type and issuer
- Order book queries
- Transaction history
- Governance proposal queries

### Query Optimization

- **Prepared Statements**: All queries use prepared statements
- **Connection Pooling**: Efficient connection management
- **Batch Operations**: Bulk operations for data loading
- **Async Operations**: Non-blocking database operations

## Monitoring and Observability

### Health Checks

- **Database Connectivity**: PostgreSQL, Redis, and Firestore health
- **Service Readiness**: Application readiness for traffic
- **Performance Metrics**: Query performance and cache hit rates

### Logging

Comprehensive logging for:
- Database operations
- Cache operations
- Migration activities
- Error conditions
- Performance metrics

## Troubleshooting

### Common Issues

**Connection Errors**:
```bash
# Check if services are running
docker-compose ps

# Check service logs
docker-compose logs postgres
docker-compose logs redis
docker-compose logs data_storage_service
```

**Migration Issues**:
```bash
# Check migration status
python manage_db.py status

# Validate migrations
python manage_db.py validate --verbose
```

**Performance Issues**:
```bash
# Check database health
python manage_db.py health

# Monitor cache performance
curl http://localhost:8003/health
```

### Recovery Procedures

**Database Recovery**:
1. Stop all services: `docker-compose down`
2. Remove volumes: `docker volume prune`
3. Restart services: `docker-compose up -d`
4. Run migrations: `python manage_db.py migrate`
5. Restore data: `python manage_db.py restore backup_file.json`

**Cache Recovery**:
1. Restart Redis: `docker-compose restart redis`
2. Cache will automatically repopulate on next requests

## Development Workflow

### Adding New Tables

1. Create migration file:
```sql
-- Add to new migration file
CREATE TABLE new_schema.new_table (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- other columns
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_new_table_field ON new_schema.new_table(field);
```

2. Run migration:
```bash
python manage_db.py migrate
```

### Adding New Repository Methods

1. Add method to appropriate repository class
2. Use `@CachedQuery` decorator for read operations
3. Implement cache invalidation for write operations
4. Add Firestore backup for critical operations

### Testing

Run the test suite:
```bash
cd ../../core/data_storage
python -m pytest tests/
```

## Production Deployment

### Environment Variables

Set production environment variables:
```bash
export POSTGRES_HOST=your-production-host
export POSTGRES_PASSWORD=your-secure-password
export REDIS_HOST=your-redis-host
export GOOGLE_CLOUD_PROJECT=your-production-project
```

### Security Hardening

1. **Database Security**:
   - Use strong passwords
   - Enable SSL connections
   - Restrict network access
   - Regular security updates

2. **Application Security**:
   - Enable API authentication
   - Configure CORS properly
   - Use HTTPS in production
   - Regular dependency updates

### Monitoring

Set up monitoring for:
- Database performance metrics
- Cache hit rates
- Error rates
- Response times
- Resource utilization

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review service logs: `docker-compose logs`
3. Validate configuration: `python manage_db.py health`
4. Create an issue in the project repository

## Contributing

When contributing to the database layer:
1. Follow the repository pattern for new data access methods
2. Include comprehensive tests for new functionality
3. Update documentation for schema changes
4. Use proper caching strategies for performance
5. Implement Firestore backup for critical operations
