FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir \
pyscf==2.6.2 \
pyqmc==0.8.1 \
numpy==1.26.4 \
scipy==1.13.1 \
h5py==3.11.0

RUN mkdir -p /app/output
