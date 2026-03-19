# The Construct - Docker Setup Guide

This guide provides comprehensive instructions for setting up and running The Construct Decentralized Robotics Exchange using Docker Compose.

## Architecture Overview

The Construct employs a microservices architecture with the following components:

### Core Services
- **Frontend**: Svelte-based web application (Port 3000)
- **Application Layer**: FastAPI backend with core business logic (Port 8080)
- **API Gateway**: Central routing and security layer (Port 8000)

### Microservices
- **Notifications Service**: Handles user notifications (Port 8001)
- **Security Service**: Authentication and authorization (Port 8002)
- **Subscription Service**: Manages user subscriptions (Port 8003)
- **Blockchain Service**: XRPL and Solana integration (Port 8004)
- **PubSub Service**: Message queue and event handling (Port 8005)
- **Injective DEX Service**: DEX integration (Port 3001)

### Infrastructure Services
- **PostgreSQL**: Primary database (Port 5432)
- **Redis**: Caching and session management (Port 6379)
- **Nginx**: Reverse proxy and load balancer (Port 80/443)

### Monitoring & Logging
- **Prometheus**: Metrics collection (Port 9090)
- **Grafana**: Metrics visualization (Port 3001)
- **Elasticsearch**: Log aggregation (Port 9200)
- **Kibana**: Log visualization (Port 5601)

## Prerequisites

- Docker Engine 20.10.0+
- Docker Compose 2.0.0+
- 8GB+ RAM recommended
- 20GB+ free disk space

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/randynolden/theConstruct.git
   cd theConstruct
   ```

2. **Create environment files**:
   ```bash
   cp application_layer/.env.example application_layer/.env
   # Edit the .env files with your configuration
   ```

3. **Start the services**:
   ```bash
   docker-compose up -d
   ```

4. **Check service status**:
   ```bash
   docker-compose ps
   ```

5. **Access the application**:
   - Frontend: http://localhost
   - API Documentation: http://localhost/api/docs
   - Grafana: http://localhost:3001 (admin/admin123)
   - Prometheus: http://localhost:9090
   - Kibana: http://localhost:5601

## Environment Configuration

### Core Environment Variables

Create or modify the following files:

#### `application_layer/.env`
```env
# Application Settings
ENVIRONMENT=development
PORT=8080
DEBUG=true

# Database
DATABASE_URL=postgresql://postgres:postgres123@postgres:5432/theconstruct_db

# Redis
REDIS_URL=redis://redis:6379

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Blockchain
SOLANA_RPC_ENDPOINT_DEVNET=https://api.devnet.solana.com
XRPL_TESTNET_URL=wss://s.altnet.rippletest.net:51233

# CORS
ALLOWED_HOSTS=localhost,127.0.0.1,frontend
```

### Production Considerations

For production deployment, update the following:

1. **Change default passwords**:
   - PostgreSQL: Update `POSTGRES_PASSWORD` in docker-compose.yml
   - Grafana: Update `GF_SECURITY_ADMIN_PASSWORD`

2. **Use secure secrets**:
   - Generate strong `SECRET_KEY` values
   - Use proper SSL certificates for nginx

3. **Configure resource limits**:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.5'
         memory: 512M
   ```

## Service Management

### Starting Services

```bash
# Start all services
docker-compose up -d

# Start specific services
docker-compose up -d postgres redis frontend

# Start with logs visible
docker-compose up
```

### Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (data loss!)
docker-compose down -v

# Stop specific service
docker-compose stop frontend
```

### Scaling Services

```bash
# Scale application service
docker-compose up -d --scale application-layer=3

# Scale with load balancer update
docker-compose up -d --scale api-gateway=2
```

## Development Workflow

### Local Development

1. **Enable development mode**:
   ```bash
   export NODE_ENV=development
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
   ```

2. **Live code reloading** is enabled through volume mounts:
   - Frontend: `./presentation_layer/the_construct_svelte:/app`
   - Backend: `./application_layer:/app`

3. **Database management**:
   ```bash
   # Access database
   docker-compose exec postgres psql -U postgres -d theconstruct_db

   # Reset database
   docker-compose down postgres
   docker volume rm theconstruct_postgres_data
   docker-compose up -d postgres
   ```

### Testing

```bash
# Run application tests
docker-compose exec application-layer python -m pytest

# Run frontend tests
docker-compose exec frontend npm test

# Integration tests
docker-compose exec application-layer python -m pytest tests/integration/
```

### Debugging

```bash
# View logs
docker-compose logs -f application-layer
docker-compose logs --tail=100 frontend

# Access container shell
docker-compose exec application-layer sh
docker-compose exec frontend sh

# Monitor resource usage
docker stats
```

## Monitoring & Observability

### Prometheus Metrics

Access metrics at http://localhost:9090

Key metrics to monitor:
- `http_requests_total` - Request count
- `http_request_duration_seconds` - Response times
- `postgres_up` - Database health
- `redis_up` - Cache health

### Grafana Dashboards

Access Grafana at http://localhost:3001 (admin/admin123)

Pre-configured dashboards:
- Application Performance
- Infrastructure Monitoring
- Blockchain Metrics
- User Activity

### Log Analysis

Access Kibana at http://localhost:5601

Log sources:
- Application logs: `/var/log/app/*.log`
- Nginx access logs: `/var/log/nginx/access.log`
- Error logs: `/var/log/nginx/error.log`

## Security Configuration

### Network Security

```yaml
# Custom network configuration
networks:
  theconstruct-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### SSL/TLS Setup

1. **Generate certificates**:
   ```bash
   mkdir -p nginx/ssl
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout nginx/ssl/theconstruct.key \
     -out nginx/ssl/theconstruct.crt
   ```

2. **Update nginx configuration** to enable HTTPS

### Security Headers

Nginx is configured with security headers:
- `X-Frame-Options: SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`
- `X-Content-Type-Options: nosniff`
- `Content-Security-Policy`

## Troubleshooting

### Common Issues

1. **Port conflicts**:
   ```bash
   # Check port usage
   netstat -tulpn | grep :3000
   
   # Modify ports in docker-compose.yml
   ```

2. **Memory issues**:
   ```bash
   # Increase Docker memory limit
   # Docker Desktop -> Settings -> Resources
   
   # Monitor memory usage
   docker stats
   ```

3. **Permission issues**:
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   
   # Check Docker permissions
   sudo usermod -aG docker $USER
   ```

4. **Database connection errors**:
   ```bash
   # Check database status
   docker-compose logs postgres
   
   # Verify connection
   docker-compose exec postgres pg_isready
   ```

### Performance Optimization

1. **Database tuning**:
   ```sql
   -- Optimize PostgreSQL settings
   ALTER SYSTEM SET shared_buffers = '256MB';
   ALTER SYSTEM SET effective_cache_size = '1GB';
   ```

2. **Redis optimization**:
   ```bash
   # Monitor Redis performance
   docker-compose exec redis redis-cli info stats
   ```

3. **Container resource limits**:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 1G
       reservations:
         memory: 512M
   ```

## Backup & Recovery

### Database Backup

```bash
# Create backup
docker-compose exec postgres pg_dump -U postgres theconstruct_db > backup.sql

# Automated backup script
./scripts/backup.sh
```

### Volume Backup

```bash
# Backup all volumes
docker run --rm -v theconstruct_postgres_data:/data \
  -v $(pwd):/backup alpine \
  tar czf /backup/postgres_backup.tar.gz /data
```

### Restore Process

```bash
# Restore database
docker-compose exec postgres psql -U postgres -d theconstruct_db < backup.sql

# Restore volumes
docker run --rm -v theconstruct_postgres_data:/data \
  -v $(pwd):/backup alpine \
  tar xzf /backup/postgres_backup.tar.gz -C /
```

## Deployment

### Production Deployment

1. **Use production compose file**:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

2. **Environment-specific configuration**:
   - Use external databases for production
   - Implement proper secret management
   - Configure external monitoring

3. **Health checks**:
   ```bash
   # Check all services
   curl http://localhost/health
   
   # Individual service health
   curl http://localhost:8080/health
   ```

### CI/CD Integration

```yaml
# Example GitHub Actions
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: |
          docker-compose pull
          docker-compose up -d
```

## Support & Contributing

### Getting Help

- Check logs: `docker-compose logs <service-name>`
- Review documentation: [docs/](docs/)
- Open issues: [GitHub Issues](https://github.com/randynolden/theConstruct/issues)

### Contributing

1. Fork the repository
2. Create a feature branch
3. Test changes with Docker Compose
4. Submit a pull request

For more information, see [CONTRIBUTING.md](CONTRIBUTING.md)
