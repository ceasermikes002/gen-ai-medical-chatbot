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
# Added timeout and max-requests settings to prevent worker issues
CMD gunicorn --workers=2 --bind 0.0.0.0:$PORT --timeout=30 --max-requests=1000 --max-requests-jitter=50 app:app


