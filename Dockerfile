# Use a slim Python image for efficiency
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system-level dependencies (needed for some pandas/numpy operations)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code
COPY . .

# Set the Python path to ensure the 'core' module is discoverable
ENV PYTHONPATH=/app

# Default command: Run the tests to ensure the container is healthy
CMD ["python3", "-m", "pytest", "--cov=core", "--cov-fail-under=100"]