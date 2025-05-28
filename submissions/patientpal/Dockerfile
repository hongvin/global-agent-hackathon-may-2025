FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make port available to the outside world
EXPOSE 7860

# Set up volume for persistent data (optional)
VOLUME ["/app/data"]

# Command to run the application
CMD ["python", "app.py"]
