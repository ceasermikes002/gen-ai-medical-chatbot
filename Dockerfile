FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=0
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run with Gunicorn - use PORT environment variable
# Added memory optimization flags for Python
CMD PYTHONUNBUFFERED=1 PYTHONOPTIMIZE=1 gunicorn --workers=1 --threads=2 --bind 0.0.0.0:$PORT --timeout=30 --max-requests=100 --max-requests-jitter=20 app:app




