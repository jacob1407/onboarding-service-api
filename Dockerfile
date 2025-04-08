FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual app code
COPY src/ ./src/

# Expose the port FastAPI will run on
EXPOSE 8080

# Run the app (note: main.py is inside src/, so we use src.main)
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
