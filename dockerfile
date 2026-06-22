# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment vars for Python:
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set workdir
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose port (FastAPI default is 8000)
EXPOSE 8000

# Default: run the FastAPI app with uvicorn
CMD ["uvicorn", "divikbox_app:app", "--host", "0.0.0.0", "--port", "8000"]
