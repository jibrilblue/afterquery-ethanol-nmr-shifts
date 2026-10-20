FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libxc-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install --no-cache-dir pyscf[libxc]==2.8.0 geometric==1.0.3 numpy==1.26.4
RUN mkdir -p /app/output
