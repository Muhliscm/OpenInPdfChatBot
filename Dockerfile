# Use the official Python slim image
FROM python:3.10-slim as base

# Set the working directory
WORKDIR /app

# Install necessary system packages, including libGL, and create a virtual environment
RUN apt update -y && \
    apt install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    python3-venv \
    awscli && \
    python3 -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code to the working directory
COPY . /app

# Activate virtual environment and install dependencies
RUN . /app/venv/bin/activate && \
    pip install -r requirements.txt && \
    rm -rf ~/.cache/pip

# Define a mount point for the PDF files
VOLUME /app/pdf_files

# Command to run the application
CMD ["/app/venv/bin/python", "app.py"]


