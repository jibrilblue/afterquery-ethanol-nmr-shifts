FROM python:3.10-slim

# Install only pytest
RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

COPY ./tests/ /tests/
RUN mkdir -p /app/output
RUN chmod 600 /tests/ground_truth.json
