FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY templates/ ./templates/

# Create necessary files
RUN touch hits.txt && \
    echo '{}' > accounts_state.json && \
    echo '{}' > settings.json

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["python", "-u", "app.py"]
