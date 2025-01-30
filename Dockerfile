FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p data/invoices data/clients data/payments data/reports data/agents data/vectors

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

# Expose port
EXPOSE 8000

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "app:app"] 
