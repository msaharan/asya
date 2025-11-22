# Dockerfile for Asya handlers
# Installs the Asya runtime and parameterises the handler entrypoint.

FROM python:3.11-slim

WORKDIR /app

# Install Asya runtime and handler dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir asya-runtime && \
    pip install --no-cache-dir -r requirements.txt

# Copy handler code
COPY handlers/ ./handlers/

# Allow overriding the handler when building individual images
ARG HANDLER="handlers.ticket_ingester.process"
ENV ASYA_HANDLER=${HANDLER}
ENV PYTHONPATH="/app"

# Asya runtime will execute the handler
CMD ["python", "-m", "asya.runtime"]
