# Python image for blockchain services
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    git

# Copy requirements file
COPY requirements.txt* ./

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org --upgrade pip && \
    pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S -D -H -u 1001 -s /sbin/nologin -G appuser appuser

# Change to non-root user
USER appuser

# Expose port
EXPOSE 8004

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8004/health')" || exit 1

# Run the blockchain service
CMD ["python", "-m", "core.service_communication.service_client"]
