FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libxc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pyscf[libxc]==2.8.0 geometric==1.0.3 pytest==8.4.1 pytest-json-ctrf==0.3.5

COPY ./tests/ /tests/
RUN mkdir -p /app/output
RUN chmod 600 /tests/ground_truth.json
