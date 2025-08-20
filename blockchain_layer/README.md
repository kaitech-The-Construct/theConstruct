# Blockchain Layer

This layer contains the blockchain integration services and smart contracts for The Construct decentralized robotics exchange. It implements a hybrid architecture leveraging both XRPL and Solana to optimize for different use cases:

- **XRPL**: Core trading, tokenization, payments, and basic escrow
- **Solana**: Advanced smart contracts for manufacturing workflows, governance, and complex business logic

The layer is designed as containerized microservices for scalability and maintainability.

## Directory Structure

### Core Services
- `services/`
  - `data_storage/`: Firestore-based off-chain metadata and transaction indexing
  - `injective_service/`: Legacy Injective integration (being phased out)
  - `solana/`: XRPL integration service for tokenization and DEX operations  
  - `spl_service/`: Solana SPL token and program interaction service
  - `trading_bot/`: Automated trading algorithms and market making
  - `oracles/`: Price feeds and external data providers

### Smart Contracts
- `services/smart_contracts/`
  - `injective/`: Legacy CosmWasm contracts (being deprecated)
  - `solana/`: Native Solana programs for advanced features
  - `test_contracts/`: Development and testing contracts

### Infrastructure
- Each service contains:
  - `src/`: Source code (TypeScript/Python/Rust)
  - `Dockerfile`: Container configuration
  - `README.md`: Service-specific documentation
  - Configuration files (`package.json`, `tsconfig.json`, etc.)

## Services Overview

### XRPL Integration (`solana/` service)
**Purpose**: Core marketplace functionality using XRPL's native features
**Responsibilities**:
- Asset tokenization (robotics components as XRPL tokens)
- DEX trading and order matching
- Basic escrow for simple purchases
- Payment processing and settlement
- Wallet integration and account management

**Technology**: Python/FastAPI with xrpl-py library

### Solana Integration (`spl_service/`)
**Purpose**: Advanced smart contract operations
**Responsibilities**:
- Complex manufacturing agreements
- Multi-party escrow with milestones
- Reputation and governance systems
- Subscription management
- Automated royalty distributions

**Technology**: TypeScript with @solana/web3.js

### Smart Contracts (`smart_contracts/solana/`)
**Purpose**: Custom Solana programs for business logic
**Key Contracts**:
- `manufacturing_workflow.rs`: Multi-milestone manufacturing orders
- `reputation_system.rs`: User reputation and ratings
- `governance.rs`: Community voting and proposals
- `subscription_manager.rs`: Recurring payment handling

**Technology**: Rust with Anchor framework

### Data Storage (`data_storage/`)
**Purpose**: Off-chain data management and indexing
**Responsibilities**:
- Product metadata and specifications
- Transaction history indexing
- User profiles and preferences
- Analytics and reporting data
- File storage for CAD designs and documentation

**Technology**: Python with Firestore integration

### Oracles (`oracles/`)
**Purpose**: External data feeds for smart contracts
**Data Sources**:
- Cryptocurrency price feeds (XRP, SOL, USD rates)
- Manufacturing cost estimates
- Shipping rates and delivery times
- Quality certification data
- Market trend analysis

### Trading Bot (`trading_bot/`)
**Purpose**: Automated market making and liquidity provision
**Functions**:
- DEX market making on XRPL
- Arbitrage opportunities
- Price stabilization
- Liquidity incentives

**Technology**: TypeScript with advanced trading algorithms

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for TypeScript services)
- Python 3.9+ (for Python services) 
- Rust and Cargo (for smart contracts)
- XRPL Testnet access
- Solana Devnet access

### Environment Configuration
```bash
# Clone the repository
git clone <repository-url>
cd blockchain_layer

# Copy environment template
cp .env.example .env

# Configure your environment variables:
# XRPL_TESTNET_URL=wss://s.altnet.rippletest.net:51233
# SOLANA_DEVNET_URL=https://api.devnet.solana.com
# PRIVATE_KEYS and wallet configurations
```

### Quick Start with Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services  
docker-compose down
```

### Individual Service Development
```bash
# XRPL Service
cd services/solana
pip install -r requirements.txt
python main.py

# Solana Service
cd services/spl_service
npm install
npm run dev

# Smart Contracts
cd services/smart_contracts/solana
anchor build
anchor deploy --provider.cluster devnet
```

## Architecture Patterns

### Service Communication
- **REST APIs**: HTTP endpoints for external communication
- **Message Queues**: Redis for async task processing
- **Event Streaming**: Real-time blockchain event processing
- **Database**: Firestore for persistence and caching

### Blockchain Interaction Patterns

#### XRPL Operations
```python
# Example: Asset tokenization
async def tokenize_robotics_component(component_data):
    # Create XRPL token with metadata
    token_response = await xrpl_client.submit(
        IssuedCurrencyAmount(
            currency=generate_currency_code(component_data.id),
            issuer=ISSUER_WALLET.address,
            value=str(component_data.quantity)
        )
    )
    return token_response
```

#### Solana Program Interaction
```typescript
// Example: Manufacturing contract call
const createManufacturingOrder = async (
    orderData: ManufacturingOrderData
) => {
    const instruction = await program.methods
        .createOrder(orderData)
        .accounts({
            order: orderAccount.publicKey,
            customer: customerWallet.publicKey,
            manufacturer: manufacturerWallet.publicKey,
        })
        .instruction();
    
    const transaction = new Transaction().add(instruction);
    return await sendAndConfirmTransaction(connection, transaction, [customerWallet]);
};
```

### Error Handling & Resilience
- **Circuit Breakers**: Prevent cascade failures
- **Retry Logic**: Exponential backoff for blockchain operations
- **Fallback Mechanisms**: Alternative chains during network issues
- **Health Checks**: Service monitoring and auto-recovery

## Testing Strategy

### Unit Tests
```bash
# Python services
pytest tests/

# TypeScript services  
npm test

# Rust smart contracts
cargo test
```

### Integration Tests
```bash
# End-to-end blockchain interactions
npm run test:integration

# Smart contract testing
anchor test
```

### Load Testing
```bash
# API performance testing
k6 run tests/load/api-load-test.js

# Blockchain throughput testing
npm run test:blockchain-load
```

## Deployment

### Development Environment
- Uses Testnet/Devnet for both chains
- Local Firestore emulator
- Docker containers for easy setup

### Staging Environment
- Testnet/Devnet with production-like data
- Cloud Firestore instance
- Kubernetes deployment on GCP

### Production Environment
- Mainnet deployment for both chains
- Multi-region redundancy
- Auto-scaling based on transaction volume
- Comprehensive monitoring and alerting

## Monitoring & Observability

### Key Metrics
- Transaction success rates
- Blockchain confirmation times
- API response times
- Error rates by service
- Resource utilization

### Logging
- Structured JSON logging
- Blockchain transaction correlation IDs
- Error tracking with stack traces
- Performance profiling data

### Alerting
- Failed transaction alerts
- Service health monitoring
- Blockchain network status
- Resource threshold warnings

## Security Considerations

### Wallet Management
- Hardware Security Modules (HSMs) for production keys
- Multi-signature requirements for high-value operations
- Key rotation policies
- Secure key storage and access controls

### Smart Contract Security
- Formal verification where possible
- Third-party security audits
- Bug bounty programs
- Gradual rollout with monitoring

### API Security
- JWT authentication
- Rate limiting per user/IP
- Input validation and sanitization
- CORS and security headers

## Contributing

See individual service README files for specific contribution guidelines. General principles:

1. **Code Quality**: Follow language-specific style guides
2. **Testing**: Maintain >80% test coverage
3. **Documentation**: Update README and inline docs
4. **Security**: Follow secure coding practices
5. **Performance**: Consider blockchain gas costs and API latency

## Support

- **Technical Issues**: Create GitHub issues with detailed reproduction steps
- **Smart Contract Bugs**: Email security@theconstruct.io immediately
- **API Questions**: Check service-specific README files first
- **Architecture Discussions**: Use GitHub Discussions