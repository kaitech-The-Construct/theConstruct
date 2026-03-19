# The Construct - Blockchain Layer

The blockchain layer provides the core infrastructure for The Construct's decentralized robotics manufacturing platform, integrating XRPL and Solana blockchains for asset tokenization, trading, and manufacturing workflow management.

## 🏗️ Architecture Overview

The blockchain layer consists of several microservices that work together to provide a comprehensive blockchain infrastructure:

- **XRPL Service**: Asset tokenization, DEX trading, and escrow management
- **SPL Service**: Solana integration for smart contracts and token operations
- **Data Storage Service**: Database management and caching layer
- **Trading Bot Service**: Automated market making and arbitrage
- **Oracle Service**: Price feeds and external data integration

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git
- curl (for health checks)

### Development Setup

1. **Clone and navigate to the blockchain layer:**
   ```bash
   cd blockchain_layer
   ```

2. **Start the development environment:**
   ```bash
   ./start-dev.sh
   ```

   This script will:
   - Create necessary configuration files
   - Start all required services
   - Initialize the database with test data
   - Perform health checks
   - Provide service URLs and useful commands

3. **Verify services are running:**
   ```bash
   docker-compose ps
   ```

## 📋 Services

### XRPL Service (Port 8001)
- **Purpose**: XRPL blockchain integration for asset tokenization and trading
- **Health Check**: `http://localhost:8001/health`
- **API Docs**: `http://localhost:8001/docs`
- **Key Features**:
  - Asset tokenization for robotics components
  - DEX order creation and management
  - Escrow services for secure transactions
  - Account and balance management

### SPL Service (Port 8002)
- **Purpose**: Solana blockchain integration for smart contracts
- **Health Check**: `http://localhost:8002/health`
- **API Docs**: `http://localhost:8002/docs`
- **Key Features**:
  - SPL token operations
  - Smart contract interactions
  - Transaction monitoring

### Data Storage Service (Port 8003)
- **Purpose**: Database operations and caching
- **Health Check**: `http://localhost:8003/health`
- **API Docs**: `http://localhost:8003/docs`
- **Key Features**:
  - PostgreSQL database management
  - Redis caching
  - Data persistence and retrieval

### Trading Bot Service (Port 8004)
- **Purpose**: Automated trading and market making
- **Features**:
  - Market making algorithms
  - Arbitrage detection
  - Risk management

### Oracle Service (Port 8005)
- **Purpose**: External data feeds and price information
- **Features**:
  - Cryptocurrency price feeds
  - Manufacturing cost data
  - Quality certification feeds

## 🗄️ Database Schema

The system uses PostgreSQL with the following schemas:

- **blockchain**: Users, assets, transactions, price feeds
- **trading**: Orders, escrows, trading history
- **manufacturing**: Orders, milestones, quality assurance
- **governance**: Proposals, votes, community decisions

### Key Tables

- `blockchain.users`: User accounts and wallet information
- `blockchain.assets`: Tokenized robotics components
- `trading.orders`: Buy/sell orders on the DEX
- `trading.escrows`: Secure transaction escrows
- `manufacturing.orders`: Manufacturing requests and progress
- `governance.proposals`: Community governance proposals

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key configuration sections:
- **Database**: PostgreSQL connection settings
- **Redis**: Cache configuration
- **XRPL**: Testnet/mainnet settings and wallet configuration
- **Solana**: Network and RPC settings
- **Services**: Inter-service communication URLs
- **Security**: JWT tokens and API keys

### Docker Compose Profiles

- **Default**: Core services (XRPL, SPL, Data Storage, Database, Redis)
- **monitoring**: Adds Prometheus and Grafana
- **local-blockchain**: Adds local Solana validator and XRPL standalone
- **production**: Adds Nginx load balancer

## 🛠️ Development

### Running Individual Services

```bash
# Start only core services
docker-compose up -d postgres redis xrpl_service

# Start with monitoring
docker-compose --profile monitoring up -d

# Start with local blockchains
docker-compose --profile local-blockchain up -d
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f xrpl_service

# Last 100 lines
docker-compose logs --tail=100 xrpl_service
```

### Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d construct_dev

# Connect to Redis
docker-compose exec redis redis-cli
```

### Service Shell Access

```bash
# Access XRPL service container
docker-compose exec xrpl_service /bin/bash

# Access database container
docker-compose exec postgres /bin/bash
```

## 🧪 Testing

### Health Checks

All services provide health check endpoints:

```bash
curl http://localhost:8001/health  # XRPL Service
curl http://localhost:8002/health  # SPL Service
curl http://localhost:8003/health  # Data Storage
```

### API Testing

Use the interactive API documentation:
- XRPL Service: http://localhost:8001/docs
- SPL Service: http://localhost:8002/docs
- Data Storage: http://localhost:8003/docs

### Sample API Calls

```bash
# Get XRPL account info
curl http://localhost:8001/api/v1/account/rTestManufacturer1234567890ABCDEF

# Get account balance
curl http://localhost:8001/api/v1/balance/rTestManufacturer1234567890ABCDEF

# Get network info
curl http://localhost:8001/api/v1/network/info

# Tokenize an asset (POST request)
curl -X POST http://localhost:8001/api/v1/tokenize \
  -H "Content-Type: application/json" \
  -d '{
    "asset_name": "Test Motor",
    "asset_description": "Test servo motor",
    "asset_type": "component",
    "quantity": 10,
    "metadata": {"test": true}
  }'
```

## 📊 Monitoring

### Prometheus Metrics

When running with the monitoring profile:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

### Service Metrics

Each service exposes metrics at `/metrics` endpoint for Prometheus scraping.

## 🔒 Security

### Development Security

- Services run with development credentials
- CORS is enabled for all origins
- Authentication is simplified for testing

### Production Considerations

- Update all default passwords
- Configure proper CORS origins
- Enable SSL/TLS
- Set up proper authentication
- Configure firewall rules
- Regular security updates

## 🚀 Deployment

### Development Deployment

The current setup is optimized for development with:
- Hot reloading enabled
- Debug logging
- Test data seeding
- Simplified authentication

### Production Deployment

For production deployment:

1. **Update environment variables**:
   - Set `ENVIRONMENT=production`
   - Configure production database URLs
   - Set secure passwords and API keys

2. **Use production profile**:
   ```bash
   docker-compose --profile production up -d
   ```

3. **Enable monitoring**:
   ```bash
   docker-compose --profile production --profile monitoring up -d
   ```

## 🔄 Data Flow

### Asset Tokenization Flow
1. User submits asset tokenization request to XRPL Service
2. XRPL Service validates asset data
3. Asset metadata stored in Data Storage Service
4. XRPL transaction created for token issuance
5. Transaction hash and asset ID returned to user

### Trading Flow
1. User creates buy/sell order via XRPL Service
2. Order stored in database via Data Storage Service
3. Trading Bot Service monitors for matching opportunities
4. Escrow created for secure transaction settlement
5. Order fulfillment triggers payment release

### Manufacturing Flow
1. Customer creates manufacturing order
2. Order stored with milestone structure
3. Manufacturer accepts and begins work
4. Progress updates trigger milestone completions
5. Quality assurance validates deliverables
6. Payments released based on milestone completion

## 🤝 Contributing

### Development Workflow

1. **Fork and clone the repository**
2. **Create a feature branch**
3. **Start development environment**: `./start-dev.sh`
4. **Make changes and test**
5. **Submit pull request**

### Code Standards

- Follow existing code structure and naming conventions
- Add comprehensive error handling
- Include unit tests for new functionality
- Update API documentation
- Follow security best practices

### Testing Requirements

- All new endpoints must have health checks
- API responses must follow standardized format
- Database changes require migration scripts
- Integration tests for critical workflows

## 📚 API Reference

### Standardized Response Format

All API responses follow this format:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { /* response data */ },
  "timestamp": "2025-01-01T12:00:00.000Z",
  "service": "xrpl_service"
}
```

Error responses:

```json
{
  "success": false,
  "message": "Error description",
  "error_code": "ERROR_CODE",
  "details": "Additional error details",
  "timestamp": "2025-01-01T12:00:00.000Z",
  "service": "xrpl_service"
}
```

## 🐛 Troubleshooting

### Common Issues

**Services won't start:**
- Check Docker is running: `docker info`
- Check port availability: `netstat -tulpn | grep :8001`
- Review logs: `docker-compose logs [service_name]`

**Database connection errors:**
- Ensure PostgreSQL is running: `docker-compose ps postgres`
- Check database logs: `docker-compose logs postgres`
- Verify connection string in `.env`

**XRPL connection issues:**
- Check XRPL testnet status
- Verify `XRPL_SERVER_URL` in `.env`
- Review XRPL service logs

**Redis connection errors:**
- Check Redis is running: `docker-compose ps redis`
- Test Redis connection: `docker-compose exec redis redis-cli ping`

### Getting Help

1. **Check service logs**: `docker-compose logs -f [service_name]`
2. **Verify service health**: `curl http://localhost:800X/health`
3. **Check database connectivity**: Connect via psql and run test queries
4. **Review configuration**: Ensure `.env` file has correct values

## 📄 License

This project is part of The Construct platform. See the main repository for license information.

## 🔗 Related Documentation

- [Application Layer Documentation](../application_layer/README.md)
- [Presentation Layer Documentation](../presentation_layer/README.md)
- [Main Project Documentation](../README.md)
- [Technical Documentation](../TECHNICAL_DOCUMENT.md)

---

**Happy Building! 🤖⚡**
