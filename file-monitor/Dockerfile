# Use official Python image as a base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY monitor.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables for directories (these will be overridden at runtime)
ENV SOURCE_DIR="/app/MonitoredFolder"
ENV DEST_DIR="/app/SecondFolder"

# Start the script
CMD ["python", "monitor.py"]
