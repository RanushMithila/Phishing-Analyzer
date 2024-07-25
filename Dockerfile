# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Install Playwright dependencies and browsers
RUN playwright install
RUN playwright install-deps

# ===============================================================================
# Create a non-root user and group with a specific UID and GID
# RUN groupadd -g 10001 appuser && useradd -u 10001 -g appuser -s /bin/sh appuser

# Change ownership of the copied files to the non-root user
# RUN chown -R appuser:appuser /app

# Switch to the non-root user
# USER 10001
# ===============================================================================

# Expose the port FastAPI is running on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
