# Use official Python image as a base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY folderCleanup.py /app/
#COPY requirements.txt /app/

# Install dependencies
#RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables for directories (these will be overridden at runtime)
ENV DEST_DIR="/app/MonitoredFolder"

# Start the script
CMD ["python", "folderCleanup.py"]