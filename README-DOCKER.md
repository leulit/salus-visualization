# SALUS Visualization Project

## Overview

Interactive visualization dashboard for SALUS project data analysis. This application provides real-time data visualization and analysis capabilities for monitoring and decision-making.

## Installation and Deployment Options

### Option 1: Docker Hub (Recommended for Production)

#### Pull and Run from Docker Hub:
```bash
# Pull the latest image
docker pull ealvarezreb/salus-visualization:latest

# Run the container
docker run -d -p 8050:8050 --name salus-app ealvarezreb/salus-visualization:latest
```

#### Using Docker Compose (Recommended):

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  salus-visualization:
    image: ealvarezreb/salus-visualization:latest
    container_name: salus-app
    ports:
      - "8050:8050"
    environment:
      - PYTHONPATH=/app
      - DASH_HOST=0.0.0.0
      - DASH_PORT=8050
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8050"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Then run:
```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 2: Build Locally

#### Prerequisites:
- Docker installed on your system
- Git for cloning the repository

#### Build and Run:
```bash
# Clone the repository
git clone https://github.com/leulit/salus-visualization.git
cd salus-visualization-main

# Build the Docker image
docker build -t salus-visualization .

# Run the container
docker run -d -p 8050:8050 --name salus-app salus-visualization
```

#### Using Docker Compose for Local Development:

Create a `docker-compose.dev.yml` file:

```yaml
version: '3.8'

services:
  salus-visualization:
    build: .
    container_name: salus-app-dev
    ports:
      - "8050:8050"
    volumes:
      - ./src:/app/src
    environment:
      - PYTHONPATH=/app
      - DASH_HOST=0.0.0.0
      - DASH_PORT=8050
    restart: unless-stopped
```

Run with:
```bash
docker-compose -f docker-compose.dev.yml up -d
```

### Option 3: Local Python Installation

```bash
# Clone the repository
git clone <repository-url>
cd salus-visualization-main

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/app.py
```

## Access the Application

Once running, open your browser and navigate to:
- **Local**: `http://localhost:8050`
- **Network**: `http://<your-server-ip>:8050`

## Docker Management Commands

### Container Management:
```bash
# View running containers
docker ps

# View all containers
docker ps -a

# Stop the container
docker stop salus-app

# Start the container
docker start salus-app

# Remove the container
docker rm salus-app

# View container logs
docker logs salus-app

# Follow logs in real-time
docker logs -f salus-app
```

### Image Management:
```bash
# List all images
docker images

# Remove local image
docker rmi salus-visualization

# Remove image from Docker Hub
docker rmi ealvarezreb/salus-visualization:latest

# Pull latest version
docker pull ealvarezreb/salus-visualization:latest
```

## Development and Publishing

### Building and Publishing Docker Image:

```bash
# Build the image
docker build -t ealvarezreb/salus-visualization:latest .

# Test locally before pushing
docker run -p 8050:8050 ealvarezreb/salus-visualization:latest

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push ealvarezreb/salus-visualization:latest

# Tag with version
docker tag ealvarezreb/salus-visualization:latest ealvarezreb/salus-visualization:v1.0
docker push ealvarezreb/salus-visualization:v1.0
```

### Environment Variables

The application supports the following environment variables:

- `PYTHONPATH`: Python path (default: `/app`)
- `DASH_HOST`: Host address (default: `0.0.0.0`)
- `DASH_PORT`: Port number (default: `8050`)
- `DATA_DIR`: Data directory path (default: `src/data`)

## Troubleshooting

### Common Issues:

1. **Port already in use:**
   ```bash
   # Check what's using port 8050
   sudo lsof -i :8050
   
   # Use a different port
   docker run -p 8051:8050 ealvarezreb/salus-visualization:latest
   ```

2. **Container won't start:**
   ```bash
   # Check container logs
   docker logs salus-app
   
   # Run interactively for debugging
   docker run -it --rm ealvarezreb/salus-visualization:latest /bin/bash
   ```

3. **Data files not found:**
   ```bash
   # Verify data directory structure
   docker exec -it salus-app ls -la src/data/
   ```

## Production Deployment

For production deployment, consider:

1. **Using Docker Compose with health checks**
2. **Setting up reverse proxy (nginx)**
3. **Implementing SSL/TLS certificates**
4. **Setting up monitoring and logging**
5. **Using environment-specific configurations**

### Sample Production docker-compose.yml:

```yaml
version: '3.8'

services:
  salus-visualization:
    image: ealvarezreb/salus-visualization:latest
    container_name: salus-production
    ports:
      - "8050:8050"
    environment:
      - PYTHONPATH=/app
      - DASH_HOST=0.0.0.0
      - DASH_PORT=8050
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8050"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - salus-visualization
    restart: unless-stopped
```

## Support

For issues and support:
1. Check the container logs: `docker logs salus-app`
2. Verify all required data files are present
3. Ensure port 8050 is available
4. Check Docker Hub for the latest image version
