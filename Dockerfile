# Use an official Python runtime as a parent image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install pybind11 and other Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory
COPY . .

# Build the C++ extensions
RUN python setup.py build_ext --inplace

# Expose the port that Flask will run on
EXPOSE 5000

# Run the Python script
CMD ["python", "main.py"]
