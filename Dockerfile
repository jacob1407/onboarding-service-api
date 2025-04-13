FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system packages (only what's needed)
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY src/ ./src/

# Expose FastAPI port
EXPOSE 8080

# Start FastAPI using Uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
