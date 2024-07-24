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

# --------------------------------------------
RUN useradd -ms /bin/bash -u 10001 rootuser && echo "rootuser:password" | chpasswd && echo "rootuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER rootuser

RUN playwright install && playwright install-deps

USER root

# Remove sudo privileges from rootuser by modifying /etc/sudoers
RUN sed -i '/rootuser ALL=(ALL) NOPASSWD:ALL/d' /etc/sudoers

# Create a normal user (if you want to switch context)
RUN usermod -G users rootuser

# Switch to the normal user (optional, if you want to switch context)
USER rootuser

# ----------------------------------------------------

# ===============================================================================
# Create a non-root user and group with a specific UID and GID
# RUN groupadd -g 10001 appuser && useradd -u 10001 -g appuser -s /bin/sh appuser

# Change ownership of the Playwright cache directory
# RUN chown -R appuser:appuser /home/root/.cache

# Change ownership of the copied files to the non-root user
# RUN chown -R appuser:appuser /app

# Switch to the non-root user
# USER 10001
# ===============================================================================

# Expose the port FastAPI is running on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
