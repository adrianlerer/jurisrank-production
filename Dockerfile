# JurisRank Production Dockerfile
# Production-ready containerization for JurisRank API

FROM python:3.11-slim

# Metadata
LABEL maintainer="Ignacio Adrian Lerer <iadrianlerer@gmail.com>"
LABEL description="JurisRank AI: Constitutional Analysis API"
LABEL version="0.3.0"

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/logs /app/prompts /app/data

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash jurisrank && \
    chown -R jurisrank:jurisrank /app
USER jurisrank

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Default command - run bibliography API
CMD ["python3", "bibliography_api.py"]

# Development mode override (use with docker run -e DEV_MODE=1)
# CMD ["python3", "mock_api_server.py"] for development