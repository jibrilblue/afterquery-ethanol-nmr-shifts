FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    libhdf5-dev \
    libxc-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN mkdir -p /app/output /app/data

# Create the reactant geometries
RUN echo "C 0.000000 0.000000 0.000000\nC 0.000000 0.000000 1.330000\nH 0.930000 0.000000 -0.380000\nH -0.930000 0.000000 -0.380000\nH 0.930000 0.000000 1.710000\nH -0.930000 0.000000 1.710000" > /app/data/ethylene.xyz

RUN echo "C 0.000000 0.000000 0.000000\nC 0.000000 0.000000 1.340000\nC 1.460000 0.000000 -0.460000\nC 1.460000 0.000000 -1.800000\nH -0.930000 0.000000 -0.380000\nH -0.930000 0.000000 1.710000\nH 1.100000 0.880000 -1.960000\nH 1.100000 -0.880000 -1.960000\nH 2.490000 0.000000 -0.100000\nH 2.490000 0.000000 -2.100000" > /app/data/butadiene.xyz
