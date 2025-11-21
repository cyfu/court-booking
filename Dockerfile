# Use an official lightweight Python image.
FROM python:3.13-slim

ENV TZ=America/Toronto

# Set the working directory in the container
WORKDIR /app

# Install uv, the package manager used by this project
RUN pip install uv

# Copy the dependency definitions and the lock file
COPY pyproject.toml uv.lock ./

# Copy the readme file, as it's required by the project build configuration
COPY README.md ./

# Copy the court configuration file
COPY court-info.json ./

# Copy the source code into the container
COPY src ./src

# Install dependencies into the system's Python environment
# --system is often preferred for Docker images to avoid venv overhead
RUN uv sync

# Set the default command to run when the container starts
# This will execute the script defined in pyproject.toml
CMD ["uv", "run", "check-availability"]
