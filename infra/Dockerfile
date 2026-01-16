FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (will be overridden by volume in dev, but good for prod)
COPY . .

# Set Python Path
ENV PYTHONPATH=/app

CMD ["python", "web/app.py"]
