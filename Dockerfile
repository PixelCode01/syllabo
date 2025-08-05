FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create app directory and user
WORKDIR /app
RUN useradd -m -u 1000 syllabo && chown -R syllabo:syllabo /app
USER syllabo

# Copy requirements first for better caching
COPY --chown=syllabo:syllabo requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=syllabo:syllabo . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Default command - interactive mode
CMD ["python", "main.py", "interactive"]