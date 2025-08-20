#!/bin/bash

# The Construct Blockchain Layer Development Startup Script

set -e

echo "🚀 Starting The Construct Blockchain Layer Development Environment"
echo "=================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from .env.example..."
    cp .env.example .env
    print_success ".env file created. Please review and update the configuration as needed."
else
    print_status ".env file already exists."
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p credentials
mkdir -p logs
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources
mkdir -p nginx

# Stop any existing containers
print_status "Stopping any existing containers..."
docker-compose down --remove-orphans

# Pull latest images
print_status "Pulling latest Docker images..."
docker-compose pull

# Build services
print_status "Building services..."
docker-compose build

# Start core services (database, redis, xrpl_service)
print_status "Starting core services..."
docker-compose up -d postgres redis xrpl_service

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 10

# Check if services are healthy
print_status "Checking service health..."
sleep 5

# Test database connection
if docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    print_success "PostgreSQL is ready"
else
    print_error "PostgreSQL is not ready"
    exit 1
fi

# Test Redis connection
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_success "Redis is ready"
else
    print_error "Redis is not ready"
    exit 1
fi

# Test XRPL service health
sleep 5
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    print_success "XRPL Service is healthy"
else
    print_warning "XRPL Service health check failed, but continuing..."
fi

# Start remaining services
print_status "Starting remaining services..."
docker-compose up -d

print_success "All services started successfully!"

echo ""
echo "🎉 Development environment is ready!"
echo "=================================="
echo ""
echo "📋 Service URLs:"
echo "  • XRPL Service:     http://localhost:8001"
echo "  • SPL Service:      http://localhost:8002"
echo "  • Data Storage:     http://localhost:8003"
echo "  • Trading Bot:      http://localhost:8004"
echo "  • Oracle Service:   http://localhost:8005"
echo "  • PostgreSQL:       localhost:5432"
echo "  • Redis:            localhost:6379"
echo ""
echo "🔍 Health Check URLs:"
echo "  • XRPL Service:     http://localhost:8001/health"
echo "  • SPL Service:      http://localhost:8002/health"
echo "  • Data Storage:     http://localhost:8003/health"
echo ""
echo "📊 API Documentation:"
echo "  • XRPL Service:     http://localhost:8001/docs"
echo "  • SPL Service:      http://localhost:8002/docs"
echo "  • Data Storage:     http://localhost:8003/docs"
echo ""
echo "🛠️  Useful Commands:"
echo "  • View logs:        docker-compose logs -f [service_name]"
echo "  • Stop services:    docker-compose down"
echo "  • Restart service:  docker-compose restart [service_name]"
echo "  • Shell access:     docker-compose exec [service_name] /bin/bash"
echo ""
echo "📝 Database Access:"
echo "  • Connect to DB:    docker-compose exec postgres psql -U postgres -d construct_dev"
echo "  • Redis CLI:        docker-compose exec redis redis-cli"
echo ""

# Optional: Start monitoring stack
read -p "🔍 Would you like to start the monitoring stack (Prometheus + Grafana)? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Starting monitoring stack..."
    docker-compose --profile monitoring up -d
    print_success "Monitoring stack started!"
    echo "  • Prometheus:       http://localhost:9090"
    echo "  • Grafana:          http://localhost:3000 (admin/admin)"
fi

# Optional: Start local blockchain networks
read -p "🔗 Would you like to start local blockchain networks (Solana + XRPL)? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Starting local blockchain networks..."
    docker-compose --profile local-blockchain up -d
    print_success "Local blockchain networks started!"
    echo "  • Solana Validator: http://localhost:8899"
    echo "  • XRPL Standalone:  http://localhost:6006"
fi

echo ""
print_success "Setup complete! Happy coding! 🎉"
echo ""
echo "💡 Tips:"
echo "  • Check the logs if any service fails to start"
echo "  • Update the .env file with your specific configuration"
echo "  • Use 'docker-compose ps' to see the status of all services"
echo "  • Run 'docker-compose down' when you're done developing"
