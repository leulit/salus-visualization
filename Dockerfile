# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for geopandas and other libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgdal-dev \
    gdal-bin \
    libproj-dev \
    proj-data \
    proj-bin \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code
COPY src/ ./src/

# Create symlink or copy data to the expected location
RUN ln -s /app/src/data /app/data || cp -r /app/src/data /app/data

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser


# Expose the port that Dash runs on
EXPOSE 8050

# Set environment variables
ENV PYTHONPATH=/app
ENV DASH_HOST=0.0.0.0
ENV DASH_PORT=8050

# Run the application
CMD ["python", "src/app.py"]