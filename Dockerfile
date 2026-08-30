FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ ./src/
COPY book-code/ ./book-code/
COPY examples/ ./examples/
COPY playground/ ./playground/
COPY scripts/ ./scripts/
COPY pyproject.toml .

# Install the package
RUN pip install --no-cache-dir -e .

# Create data directories
RUN mkdir -p /app/data/chroma /app/logs

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python", "-m", "agentic_patterns"]
