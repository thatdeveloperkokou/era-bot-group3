FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy and make start script executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Set default PORT (cloud platforms like Render/Railway will override this at runtime)
ENV PORT=5000

# Expose port (cloud platforms set PORT dynamically)
EXPOSE 5000

# Run the application via start.sh which expands PORT safely
# Use shell form to ensure cloud platforms can expand PORT variable
CMD sh -c "/app/start.sh"

