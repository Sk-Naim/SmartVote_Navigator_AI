# Use official lightweight Python image
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set working directory
WORKDIR /app

# Install dependencies spanning across the layers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image.
COPY src/ /app/src/

# Use uvicorn with a single worker suitable for Cloud Run scaling
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
