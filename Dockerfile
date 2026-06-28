# Use the official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /code

# Install system dependencies required for building psycopg2 if needed
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker caching layers
COPY ./requirements.txt /code/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the entire app directory into the container
COPY ./app /code/app
COPY ./main.py /code/main.py

# Expose the port FastAPI will run on
EXPOSE 8000

# Start command running Uvicorn tied to host 0.0.0.0 so the external cloud can reach it
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]