# Base image
FROM python:3.10-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libatlas-base-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libhdf5-103 \
    python3-dev \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Optional: Pre-train a model if necessary
# RUN python pipeline/training_pipeline.py

# Expose port (FastAPI default)
EXPOSE 8000

# Run FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]