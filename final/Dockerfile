FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install gcloud CLI for authentication
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH=$PATH:/root/google-cloud-sdk/bin

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

# Copy application code
COPY . .

# Switch to non-root user
USER appuser

# Expose port (Cloud Run will provide PORT env var)
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]
