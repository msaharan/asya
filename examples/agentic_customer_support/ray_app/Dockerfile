# Dockerfile for Ray Serve deployment
FROM rayproject/ray:2.9.0-py311

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY handlers/ ./handlers/
COPY serve/ ./serve/

ENV PYTHONPATH="/app"

# Start Ray Serve
CMD ["ray", "serve", "start", "--host", "0.0.0.0", "serve.pipeline:build_app"]
